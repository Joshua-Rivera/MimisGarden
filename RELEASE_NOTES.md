# Local release verification

The local release is running through Docker Compose at http://127.0.0.1:5500.

## Delivered

- Trained EfficientNet-B0 checkpoint with the existing three-class contract.
- Exact-deduplicated train/validation/test manifests without modifying source images.
- Real, cached CPU inference with matching image preprocessing and validated labels.
- Live model metrics, administrator-only history, protected review images, and correction forms.
- Bounded image validation, prediction rate limiting, private administrator credentials, and request logging.
- Persistent container storage, consistent SQLite backups, reviewed-image export, and retention preview/apply commands.
- Pinned Python dependencies, frontend production build, and a GitHub Actions check workflow.
- Setup, operation, deployment, and model limitation documentation.

## Results

Three training epochs completed on Apple MPS. The selected checkpoint is epoch 3.

- Validation: 8,060 images; accuracy 98.72%, weighted F1 0.9872.
- Held-out test: 8,063 images; accuracy 98.93%, weighted F1 0.9893, macro F1 0.9888.
- Local automated regression suite: 9 tests passed.
- Frontend type check and production build: passed.
- Backend and frontend container builds: passed after retrying an interrupted dependency download.
- Container HTTP smoke test: page, health, readiness, actual inference, authorization, protected image, review, and metrics passed.
- Backend restart: model readiness recovered and the saved prediction persisted.
- Browser checks: real upload-to-result flow, invalid administrator access, live checkpoint metrics, and mobile layout.

Test results describe the same source dataset, not independent real garden photos. Exact duplicates were excluded; near duplicates and plant-level grouping remain unverified. See `backend/app/ml/reports/MODEL_CARD.md` for the complete model scope and results.

## Access and remaining external work

The root `.env` contains a generated local administrator token, is ignored by Git, and has owner-only file permissions. Use that value in the Manage section. Do not place it in frontend configuration or public messages.

Public Vercel/Railway deployment has not been performed: no local credentials or linked hosting project configuration were available. The deployment files and instructions are prepared. Publishing needs authenticated access, persistent storage, the trained checkpoint, and the hosting environment settings described in the README.

No claim of broad real-world model accuracy is made. A separately collected and reviewed set of actual garden photos is still needed before making that claim. No automatic retention deletion is enabled; cleanup is an explicit maintenance action.
