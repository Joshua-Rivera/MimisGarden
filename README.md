# Mimi's Garden

Upload a leaf photo to classify its visible condition as **healthy**, **leaf spots**, or **severe damage**. The React/Vite interface calls a FastAPI service backed by an EfficientNet-B0 checkpoint. Low-confidence results enter an administrator review queue.

This is broad visual-condition guidance, not identification of a specific disease. The model cannot establish the cause of damage, guarantee that a plant is healthy, or reliably reject every non-plant photo. Scores from the source dataset do not establish performance on real garden photos.

## Run locally

The repository uses Python 3.13 and Node 22. From the repository root:

```sh
python3.13 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements-dev.txt
npm --prefix frontend ci
cp backend/.env.example backend/.env.local
```

Replace the example administrator token in `backend/.env.local` with a long random value. Never put that token in a frontend build variable or commit it. The release work created a separate private root `.env` for Docker; use its token for the Docker administration screen.

A trained checkpoint must be installed at `backend/app/ml/models/plant_model_v1.pt`, or set `MODEL_PATH` to its absolute path. Checkpoints and datasets are intentionally excluded from Git. The locally trained checkpoint is already in that location after a successful training run.

Start the backend from `backend`:

```sh
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --env-file .env.local
```

Start the frontend from another terminal at the repository root:

```sh
npm --prefix frontend run dev
```

Open http://localhost:5500. The Manage section accepts the administrator token and shows actual prediction history, summary metrics, and review images. Tokens remain in page memory. Reviewers must explicitly select a condition; unclear or unsupported images are excluded from training exports.

## Train and evaluate

Install `backend/requirements-training.txt` when training outside the development environment. Existing image interfaces are preserved:

```text
backend/app/ml/data/train/{healthy,leaf_spots,severe_damage}/
backend/app/ml/data/val/{healthy,leaf_spots,severe_damage}/
```

Run from the repository root:

```sh
backend/.venv/bin/python backend/app/ml/audit_dataset.py
backend/.venv/bin/python backend/app/ml/training/train_cnn.py --epochs 3 --warmup-epochs 1 --workers 4
```

The audit hashes images, removes exact duplicates from the manifests, excludes train/validation overlap, and divides the original validation images into disjoint validation and test subsets per class. It leaves every source image untouched. Run it again after changing the dataset. It does not detect perceptual duplicates or identify different photos of the same plant.

The trainer uses ImageNet weights, a replacement classifier, classifier-only warmup, then full fine-tuning with a lower backbone learning rate. Defaults are 10 total epochs and 2 warmup epochs; the command above is a shorter first-release baseline. It chooses CUDA, Apple MPS, or CPU; mixed precision is enabled on CUDA. It saves the best validation weighted-F1 checkpoint, including labels, class indices, preprocessing, optimizer state, epoch, and metrics. Training history is written to `backend/app/ml/reports/training_history.json`. The first run downloads pretrained weights.

After selecting the checkpoint, evaluate from `backend`:

```sh
.venv/bin/python -m app.ml.evaluate_model
```

Results go to `backend/app/ml/reports/test_evaluation.json`, including per-class precision/recall/F1, confusion matrix, and confidence-threshold coverage. Do not tune against this test set. Before claiming real-world accuracy, collect a separate set of real garden photos, verify labels with knowledgeable reviewers, and evaluate those independently. Confidence scores are not calibrated probabilities of correctness.

The existing raw-data preparation script is optional. Review its source mapping before using it: it groups source diseases into broad visual conditions. The release training uses the existing prepared folders directly.

## Containers

From the root, copy `.env.example` to `.env` if `.env` does not exist and set a random `ADMIN_TOKEN`. Keep the checkpoint at the model path above.

```sh
docker compose up --build -d
```

Open http://localhost:5500. Nginx serves the built frontend and proxies API requests to the backend. A named volume persists the SQLite database and uploaded images. Model files are mounted read-only. Neither datasets nor credentials are included in the image. The root Compose configuration binds the website to localhost; external hosting needs a TLS reverse proxy or managed HTTPS endpoint.

For Railway or another container host, build `backend/Dockerfile` with the **repository root** as the context. Supply persistent `STORAGE_DIR`, a mounted checkpoint via `MODEL_PATH`, a secret `ADMIN_TOKEN`, and the correct `CORS_ORIGINS`. For Vercel, use `frontend` as the project root, the Vite build, `dist` output, and an HTTPS `VITE_API_BASE_URL`. A Docker frontend uses same-origin `/api/v1` automatically.

The backend serves CPU inference with one cached model per process. Restart it after replacing the checkpoint. `/health` checks the service; `/ready` additionally checks that a compatible model can load. Liveness deliberately remains successful when a model is missing; use readiness for deployment acceptance. Do not expose a model-less deployment as ready.

## API

- `POST /api/v1/predict`: multipart `file`; JPG/PNG/WebP, up to 5 MB and 20 megapixels.
- `GET /api/v1/models/current`: actual loaded checkpoint metadata.
- `GET /api/v1/predictions?limit=50&offset=0`: administrator-only history.
- `GET /api/v1/metrics/summary`: administrator-only usage metrics.
- `GET /api/v1/reviews`: administrator-only pending queue, at most 100 records.
- `GET /api/v1/reviews/{prediction_id}/image`: protected image access.
- `POST /api/v1/reviews/{prediction_id}`: corrected label and optional notes.

Administrative calls require `Authorization: Bearer <ADMIN_TOKEN>`. When no token is configured, these endpoints fail closed. Public prediction requests are limited to ten per minute per direct client address in one worker. Compose trusts its internal proxy, which overwrites the forwarded client address; the backend has no exposed host port. For a public multi-worker deployment, enforce shared limits at the reverse proxy and configure trusted proxy addresses; the in-process limiter alone is not a distributed abuse-control system. The app does not implement user accounts or personal history.

## Review exports, retention, and backups

Run these commands from `backend` using the same storage/database settings as the API:

```sh
.venv/bin/python -m app.maintenance export-reviews /absolute/path/to/review-export
.venv/bin/python -m app.maintenance backup /absolute/path/to/new-backup.db
.venv/bin/python -m app.maintenance purge --days 30
```

For the container deployment, run the same commands with `docker compose exec backend python -m app.maintenance ...` and use a destination under `/srv/storage` so exports and backups survive container replacement.

Exports contain reviewed, supported labels and hashed image names. They are **not** automatically mixed into training: audit labels, duplicates, and data splits first. The backup command uses SQLite's consistent backup API; also back up uploaded images and model files. Test restoration before relying on backups.

Purge previews eligible records by default. Add `--apply` to delete them; reviewed records are retained unless `--include-reviewed` is supplied. Export reviewed samples before deleting them. No automatic deletion is enabled. Decide and publish your retention policy before accepting public uploads.

SQLite tables are created on startup and the existing schema is preserved. Future schema changes require an explicit migration and a backup; startup table creation does not migrate existing columns.

## Verification

From `backend`:

```sh
.venv/bin/python -m unittest discover -s tests -v
```

From the repository root:

```sh
npm --prefix frontend run build
```

Tests isolate the database and uploads. They cover authorization, rate limiting, image rejection, failed-inference cleanup, prediction/review/metrics flow, real checkpoint contracts, transfer-learning gradients, and duplicate-safe manifests. CI repeats the backend suite and frontend build. Runtime request logs contain status, duration, and request ID without logging uploaded image contents or administrator tokens.

Generated source-dataset folders contain legacy third-party scripts and are excluded from release packaging. They are not part of the application test suite.
