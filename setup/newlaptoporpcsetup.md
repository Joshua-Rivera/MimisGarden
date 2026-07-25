### NEW DEVICE SETUP FOR PERSONAL REFERENCE AND USE ONLY, SPECIFICALLY MACOS ###
# Mimi's PlantHealth Ops — macOS + VS Code Setup

This guide configures the Mimi’s Garden project for development on macOS using Visual Studio Code.

It includes:

* Python virtual environment
* FastAPI backend dependencies
* PyTorch installation
* Apple Metal Performance Shaders support
* React/Vite frontend dependencies
* VS Code interpreter configuration
* VS Code debugging and tasks
* SQLite configuration
* Testing tools
* Common troubleshooting

Run the commands using the VS Code integrated terminal:

```text
Terminal → New Terminal
```

---

# 1. Expected Project Structure

Open the main `MimisGarden` folder in VS Code.

```text
MimisGarden/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── services/
│   │   ├── models/
│   │   └── ...
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   └── src/
├── .vscode/
└── .gitignore
```

This setup assumes that the FastAPI application is located at:

```text
backend/app/main.py
```

and contains an application object similar to:

```python
from fastapi import FastAPI

app = FastAPI(
    title="Mimi's PlantHealth Ops API",
    version="0.1.0",
)
```

The Uvicorn application entry point will therefore be:

```text
app.main:app
```

---

# 2. Confirm the Correct Project Folder Is Open

In the VS Code terminal, run:

```bash
pwd
ls
```

You should see:

```text
backend
frontend
```

If those folders are not visible, open the correct project folder:

```bash
code /path/to/MimisGarden
```

Example:

```bash
code ~/Documents/MimisGarden
```

---

# 3. Install Apple Command Line Tools

Run:

```bash
xcode-select --install
```

If the tools are already installed, macOS may tell you that no installation is necessary.

Verify them with:

```bash
xcode-select -p
```

A normal result is:

```text
/Library/Developer/CommandLineTools
```

---

# 4. Install Homebrew

Check whether Homebrew is installed:

```bash
brew --version
```

If the command is not found, install Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Apple Silicon Mac

Add Homebrew to the current terminal:

```bash
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Add it permanently to Zsh:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

## Intel Mac

Add Homebrew to the current terminal:

```bash
eval "$(/usr/local/bin/brew shellenv)"
```

Add it permanently to Zsh:

```bash
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

---

# 5. Install System Development Tools

Run:

```bash
brew update

brew install \
  python@3.13 \
  node \
  git \
  git-lfs \
  gh \
  cmake \
  ninja \
  make \
  pkgconf \
  sqlite \
  jq \
  tree
```

Optional development applications:

```bash
brew install --cask \
  docker-desktop \
  postman \
  dbeaver-community
```

Verify the installations:

```bash
python3 --version
node --version
npm --version
git --version
gh --version
cmake --version
```

---

# 6. Complete Automatic Mimi’s Garden Setup

Run this entire block from the main `MimisGarden` project folder.

```bash
cat > setup_mimis_garden_macos.sh <<'SETUP'
#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
VENV_DIR="$BACKEND_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"

echo "=============================================="
echo " Mimi's PlantHealth Ops — macOS Setup"
echo "=============================================="
echo "Project root: $PROJECT_ROOT"

# --------------------------------------------------
# Validate project folders
# --------------------------------------------------

if [[ ! -d "$BACKEND_DIR" ]]; then
    echo "ERROR: backend/ was not found."
    echo "Open the main MimisGarden folder and try again."
    exit 1
fi

if [[ ! -d "$FRONTEND_DIR" ]]; then
    echo "ERROR: frontend/ was not found."
    echo "Open the main MimisGarden folder and try again."
    exit 1
fi

# --------------------------------------------------
# Validate required programs
# --------------------------------------------------

for command in python3 node npm git; do
    if ! command -v "$command" >/dev/null 2>&1; then
        echo "ERROR: $command is not installed or not available in PATH."
        exit 1
    fi
done

echo ""
echo "Detected programs:"
echo "Python: $(python3 --version)"
echo "Node:   $(node --version)"
echo "npm:    $(npm --version)"
echo "Git:    $(git --version)"

# --------------------------------------------------
# Create backend Python environment
# --------------------------------------------------

echo ""
echo "Creating backend Python environment..."

if [[ ! -d "$VENV_DIR" ]]; then
    python3 -m venv "$VENV_DIR"
else
    echo "Existing backend/.venv found."
fi

if [[ ! -x "$VENV_PYTHON" ]]; then
    echo "ERROR: The virtual environment was not created correctly."
    exit 1
fi

"$VENV_PYTHON" -m pip install --upgrade \
    pip \
    setuptools \
    wheel

# --------------------------------------------------
# Install FastAPI backend dependencies
# --------------------------------------------------

echo ""
echo "Installing backend dependencies..."

"$VENV_PYTHON" -m pip install \
    "fastapi[standard]" \
    "uvicorn[standard]" \
    sqlalchemy \
    alembic \
    pydantic \
    pydantic-settings \
    python-multipart \
    python-dotenv \
    aiofiles \
    httpx \
    requests

# --------------------------------------------------
# Install image and data dependencies
# --------------------------------------------------

echo ""
echo "Installing image and data dependencies..."

"$VENV_PYTHON" -m pip install \
    pillow \
    numpy \
    pandas \
    scipy \
    scikit-learn \
    matplotlib \
    opencv-python \
    tqdm \
    joblib

# --------------------------------------------------
# Install PyTorch
# --------------------------------------------------

echo ""
echo "Installing PyTorch and Torchvision..."

"$VENV_PYTHON" -m pip install \
    torch \
    torchvision

# --------------------------------------------------
# Install testing and code-quality tools
# --------------------------------------------------

echo ""
echo "Installing testing and code-quality tools..."

"$VENV_PYTHON" -m pip install \
    pytest \
    pytest-asyncio \
    pytest-cov \
    black \
    ruff \
    mypy

# --------------------------------------------------
# Install existing project requirements
# --------------------------------------------------

if [[ -f "$BACKEND_DIR/requirements.txt" ]]; then
    echo ""
    echo "Installing backend/requirements.txt..."

    "$VENV_PYTHON" -m pip install \
        -r "$BACKEND_DIR/requirements.txt"
fi

# Save a complete macOS dependency list.

"$VENV_PYTHON" -m pip freeze \
    > "$BACKEND_DIR/requirements-macos.txt"

# --------------------------------------------------
# Create runtime directories
# --------------------------------------------------

echo ""
echo "Creating runtime directories..."

mkdir -p \
    "$BACKEND_DIR/storage/uploaded_images" \
    "$BACKEND_DIR/storage/models" \
    "$BACKEND_DIR/logs"

touch "$BACKEND_DIR/storage/uploaded_images/.gitkeep"
touch "$BACKEND_DIR/storage/models/.gitkeep"
touch "$BACKEND_DIR/logs/.gitkeep"

# --------------------------------------------------
# Create backend environment file
# --------------------------------------------------

if [[ ! -f "$BACKEND_DIR/.env" ]]; then
    cat > "$BACKEND_DIR/.env" <<'BACKEND_ENV'
APP_NAME=Mimi's PlantHealth Ops API
APP_VERSION=0.1.0
APP_ENV=development
DEBUG=true

DATABASE_URL=sqlite:///./mimis_planthealth.db

UPLOAD_DIRECTORY=storage/uploaded_images
MODEL_DIRECTORY=storage/models
MODEL_VERSION=development-model

CONFIDENCE_THRESHOLD=0.70
REVIEW_THRESHOLD=0.50

ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
BACKEND_ENV

    echo "Created backend/.env"
else
    echo "Existing backend/.env preserved."
fi

# --------------------------------------------------
# Install frontend dependencies
# --------------------------------------------------

echo ""
echo "Installing frontend dependencies..."

cd "$FRONTEND_DIR"

if [[ ! -f package.json ]]; then
    echo "ERROR: frontend/package.json was not found."
    exit 1
fi

if [[ -f package-lock.json ]]; then
    npm ci
else
    npm install
fi

npm list axios >/dev/null 2>&1 || npm install axios
npm list animejs >/dev/null 2>&1 || npm install animejs

npm list @rive-app/react-canvas >/dev/null 2>&1 || \
    npm install @rive-app/react-canvas

# --------------------------------------------------
# Create frontend environment file
# --------------------------------------------------

if [[ ! -f "$FRONTEND_DIR/.env" ]]; then
    cat > "$FRONTEND_DIR/.env" <<'FRONTEND_ENV'
VITE_API_BASE_URL=http://127.0.0.1:8000
FRONTEND_ENV

    echo "Created frontend/.env"
else
    echo "Existing frontend/.env preserved."
fi

# --------------------------------------------------
# Create VS Code configuration
# --------------------------------------------------

echo ""
echo "Creating VS Code configuration..."

mkdir -p "$PROJECT_ROOT/.vscode"

cat > "$PROJECT_ROOT/.vscode/settings.json" <<'JSON'
{
    "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.analysis.extraPaths": [
        "${workspaceFolder}/backend"
    ],
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "backend/tests"
    ],
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit"
        }
    },
    "[javascript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.formatOnSave": true
    },
    "[javascriptreact]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.formatOnSave": true
    },
    "[typescript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.formatOnSave": true
    },
    "[typescriptreact]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.formatOnSave": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true,
        "**/.ruff_cache": true
    }
}
JSON

cat > "$PROJECT_ROOT/.vscode/extensions.json" <<'JSON'
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "ms-python.vscode-python-envs",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        "ms-toolsai.jupyter",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-azuretools.vscode-docker",
        "ms-vscode-remote.remote-containers",
        "github.vscode-pull-request-github",
        "redhat.vscode-yaml"
    ]
}
JSON

cat > "$PROJECT_ROOT/.vscode/launch.json" <<'JSON'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Mimi's Garden Backend",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload",
                "--host",
                "127.0.0.1",
                "--port",
                "8000"
            ],
            "cwd": "${workspaceFolder}/backend",
            "envFile": "${workspaceFolder}/backend/.env",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
JSON

cat > "$PROJECT_ROOT/.vscode/tasks.json" <<'JSON'
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Mimi's Garden: Run Backend",
            "type": "shell",
            "command": "${workspaceFolder}/backend/.venv/bin/python",
            "args": [
                "-m",
                "uvicorn",
                "app.main:app",
                "--reload",
                "--host",
                "127.0.0.1",
                "--port",
                "8000"
            ],
            "options": {
                "cwd": "${workspaceFolder}/backend"
            },
            "problemMatcher": []
        },
        {
            "label": "Mimi's Garden: Run Frontend",
            "type": "npm",
            "script": "dev",
            "path": "frontend",
            "problemMatcher": []
        },
        {
            "label": "Mimi's Garden: Run Backend Tests",
            "type": "shell",
            "command": "${workspaceFolder}/backend/.venv/bin/python",
            "args": [
                "-m",
                "pytest",
                "-v"
            ],
            "options": {
                "cwd": "${workspaceFolder}/backend"
            },
            "problemMatcher": []
        }
    ]
}
JSON

# --------------------------------------------------
# Configure .gitignore
# --------------------------------------------------

cd "$PROJECT_ROOT"
touch .gitignore

add_gitignore_entry() {
    local entry="$1"

    if ! grep -Fqx "$entry" .gitignore; then
        echo "$entry" >> .gitignore
    fi
}

add_gitignore_entry ""
add_gitignore_entry "# Python"
add_gitignore_entry "backend/.venv/"
add_gitignore_entry "**/__pycache__/"
add_gitignore_entry "*.py[cod]"
add_gitignore_entry ".pytest_cache/"
add_gitignore_entry ".mypy_cache/"
add_gitignore_entry ".ruff_cache/"

add_gitignore_entry ""
add_gitignore_entry "# Environment files"
add_gitignore_entry "backend/.env"
add_gitignore_entry "frontend/.env"

add_gitignore_entry ""
add_gitignore_entry "# Databases"
add_gitignore_entry "*.db"
add_gitignore_entry "*.sqlite"
add_gitignore_entry "*.sqlite3"

add_gitignore_entry ""
add_gitignore_entry "# Runtime files"
add_gitignore_entry "backend/storage/uploaded_images/*"
add_gitignore_entry "!backend/storage/uploaded_images/.gitkeep"
add_gitignore_entry "backend/storage/models/*"
add_gitignore_entry "!backend/storage/models/.gitkeep"
add_gitignore_entry "backend/logs/*"
add_gitignore_entry "!backend/logs/.gitkeep"

add_gitignore_entry ""
add_gitignore_entry "# Frontend"
add_gitignore_entry "frontend/node_modules/"
add_gitignore_entry "frontend/dist/"

add_gitignore_entry ""
add_gitignore_entry "# macOS"
add_gitignore_entry ".DS_Store"

# --------------------------------------------------
# Verify backend packages
# --------------------------------------------------

echo ""
echo "Verifying backend packages..."

"$VENV_PYTHON" - <<'PYTHON'
import platform

import fastapi
import numpy
import PIL
import sklearn
import sqlalchemy
import torch
import torchvision

print(f"Python:        {platform.python_version()}")
print(f"FastAPI:       {fastapi.__version__}")
print(f"SQLAlchemy:    {sqlalchemy.__version__}")
print(f"NumPy:         {numpy.__version__}")
print(f"Pillow:        {PIL.__version__}")
print(f"scikit-learn:  {sklearn.__version__}")
print(f"PyTorch:       {torch.__version__}")
print(f"Torchvision:   {torchvision.__version__}")
print(f"MPS built:     {torch.backends.mps.is_built()}")
print(f"MPS available: {torch.backends.mps.is_available()}")
PYTHON

echo ""
echo "=============================================="
echo " Setup complete"
echo "=============================================="
echo ""
echo "Backend interpreter:"
echo "$VENV_PYTHON"
echo ""
echo "Reload VS Code and select this interpreter:"
echo "backend/.venv/bin/python"
echo ""
echo "Run backend:"
echo "cd backend"
echo "source .venv/bin/activate"
echo "python -m uvicorn app.main:app --reload"
echo ""
echo "Run frontend:"
echo "cd frontend"
echo "npm run dev"
SETUP

chmod +x setup_mimis_garden_macos.sh
./setup_mimis_garden_macos.sh
```

---

# 7. Reload VS Code

Open the Command Palette:

```text
Shift + Command + P
```

Run:

```text
Developer: Reload Window
```

---

# 8. Select the Mimi’s Garden Python Interpreter

Open the Command Palette:

```text
Shift + Command + P
```

Select:

```text
Python: Select Interpreter
```

Choose:

```text
MimisGarden/backend/.venv/bin/python
```

If it is not listed:

1. Select `Enter interpreter path`
2. Select `Find`
3. Navigate to:

```text
backend/.venv/bin/python
```

---

# 9. Verify the Selected Interpreter

Open a new VS Code terminal after selecting the interpreter.

Run:

```bash
which python
python --version
python -m pip --version
```

The Python and pip paths should contain:

```text
MimisGarden/backend/.venv
```

Example:

```text
/Users/your-name/Documents/MimisGarden/backend/.venv/bin/python
```

---

# 10. Verify PyTorch

Run:

```bash
python -c "import torch; print('PyTorch:', torch.__version__); print('MPS built:', torch.backends.mps.is_built()); print('MPS available:', torch.backends.mps.is_available())"
```

On a compatible Apple Silicon Mac, the result should resemble:

```text
PyTorch: 2.x.x
MPS built: True
MPS available: True
```

An Intel Mac or unsupported configuration may return:

```text
MPS available: False
```

The application can still use the CPU.

---

# 11. Fix `No module named 'torch'`

The following error:

```text
ModuleNotFoundError: No module named 'torch'
```

means PyTorch was not installed in the Python environment that ran the command.

From the main `MimisGarden` folder, run:

```bash
backend/.venv/bin/python -m pip install --upgrade pip
backend/.venv/bin/python -m pip install torch torchvision
```

Verify it using the same interpreter:

```bash
backend/.venv/bin/python -c "import torch; print('PyTorch:', torch.__version__); print('MPS available:', torch.backends.mps.is_available())"
```

Alternatively, activate the environment first:

```bash
cd backend
source .venv/bin/activate

python -m pip install torch torchvision

python -c "import torch; print('PyTorch:', torch.__version__); print('MPS available:', torch.backends.mps.is_available())"
```

Prefer this installation form:

```bash
python -m pip install PACKAGE_NAME
```

Avoid relying on plain `pip install` because `pip` can occasionally point to a different Python installation.

---

# 12. Start the Backend

Open the first VS Code terminal:

```bash
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload
```

The backend should start at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative command without activating the environment:

```bash
backend/.venv/bin/python -m uvicorn app.main:app --reload --app-dir backend
```

If `app.main:app` fails, inspect the backend structure:

```bash
find backend -maxdepth 3 -type f | sort
```

If the application is located directly at:

```text
backend/main.py
```

run:

```bash
cd backend
source .venv/bin/activate
python -m uvicorn main:app --reload
```

---

# 13. Start the Frontend

Open a second VS Code terminal:

```bash
cd frontend
npm run dev
```

The Vite frontend normally starts at:

```text
http://localhost:5173
```

The frontend environment file should contain:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Restart the frontend development server after changing `.env`.

---

# 14. Test Backend Imports

Run:

```bash
cd backend
source .venv/bin/activate

python -c "
import fastapi
import sqlalchemy
import pydantic
import PIL
import numpy
import sklearn
import torch
import torchvision

print('All core imports succeeded.')
"
```

---

# 15. Run Backend Tests

From `backend/`:

```bash
source .venv/bin/activate
python -m pytest -v
```

Run tests with coverage:

```bash
python -m pytest \
  --cov=app \
  --cov-report=term-missing
```

You can also use the VS Code task:

```text
Terminal
→ Run Task
→ Mimi's Garden: Run Backend Tests
```

---

# 16. Apple MPS Device Selection

Use this pattern in the model code:

```python
import torch


def select_device() -> torch.device:
    if torch.backends.mps.is_available():
        return torch.device("mps")

    if torch.cuda.is_available():
        return torch.device("cuda")

    return torch.device("cpu")


device = select_device()

print(f"Using device: {device}")
```

Move the model to the selected device:

```python
model = model.to(device)
```

Move input tensors to the same device:

```python
images = images.to(device)
labels = labels.to(device)
```

Example inference:

```python
import torch


device = select_device()

model = model.to(device)
model.eval()

with torch.no_grad():
    images = images.to(device)
    predictions = model(images)
```

Important:

* Apple Silicon Macs use `mps`.
* Windows and Linux systems with compatible NVIDIA GPUs use `cuda`.
* Systems without an available accelerator use `cpu`.
* Keep a CPU fallback because some PyTorch operations may not support MPS.

---

# 17. Recommended `backend/requirements.txt`

Create or update:

```text
backend/requirements.txt
```

Recommended content:

```text
fastapi[standard]
uvicorn[standard]
sqlalchemy
alembic
pydantic
pydantic-settings
python-multipart
python-dotenv
aiofiles
httpx
requests
pillow
numpy
pandas
scipy
scikit-learn
matplotlib
opencv-python
tqdm
joblib
torch
torchvision
pytest
pytest-asyncio
pytest-cov
black
ruff
mypy
```

Install it with:

```bash
cd backend
source .venv/bin/activate

python -m pip install \
  -r requirements.txt
```

Capture the exact installed package versions:

```bash
python -m pip freeze \
  > requirements-lock.txt
```

---

# 18. Recommended Backend Environment File

Create:

```text
backend/.env
```

Content:

```env
APP_NAME=Mimi's PlantHealth Ops API
APP_VERSION=0.1.0
APP_ENV=development
DEBUG=true

DATABASE_URL=sqlite:///./mimis_planthealth.db

UPLOAD_DIRECTORY=storage/uploaded_images
MODEL_DIRECTORY=storage/models
MODEL_VERSION=development-model

CONFIDENCE_THRESHOLD=0.70
REVIEW_THRESHOLD=0.50

ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Do not commit `.env` files that contain passwords, API keys, or other secrets.

---

# 19. Recommended Frontend Environment File

Create:

```text
frontend/.env
```

Content:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Use the variable in React:

```javascript
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
```

Example Axios configuration:

```javascript
import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
});

export default apiClient;
```

---

# 20. VS Code Commands

Open the Command Palette:

```text
Shift + Command + P
```

Useful commands:

```text
Python: Select Interpreter
Python: Create Terminal
Developer: Reload Window
Tasks: Run Task
Debug: Select and Start Debugging
Extensions: Show Recommended Extensions
```

To start the FastAPI debugger:

1. Open `Run and Debug`
2. Select `Mimi's Garden Backend`
3. Press the green Run button

---

# 21. Common Troubleshooting

## `ModuleNotFoundError`

Check the active Python:

```bash
which python
python --version
python -m pip --version
```

Check whether a package is installed:

```bash
python -m pip show torch
```

Install it into the active interpreter:

```bash
python -m pip install torch torchvision
```

Install using the guaranteed project interpreter:

```bash
backend/.venv/bin/python -m pip install \
  torch \
  torchvision
```

---

## VS Code Selects the Wrong Python

Make sure the selected interpreter is:

```text
backend/.venv/bin/python
```

Then:

1. Close the existing terminal
2. Open a new terminal
3. Run:

```bash
which python
```

You can also reload VS Code:

```text
Shift + Command + P
Developer: Reload Window
```

---

## Recreate a Damaged Virtual Environment

From the project root:

```bash
rm -rf backend/.venv

python3 -m venv backend/.venv

backend/.venv/bin/python -m pip install --upgrade \
  pip \
  setuptools \
  wheel

backend/.venv/bin/python -m pip install \
  -r backend/requirements.txt
```

Verify:

```bash
backend/.venv/bin/python -c \
"import torch; print(torch.__version__)"
```

---

## `uvicorn: command not found`

Run Uvicorn as a Python module:

```bash
python -m uvicorn app.main:app --reload
```

Or use the project interpreter directly:

```bash
backend/.venv/bin/python \
  -m uvicorn \
  app.main:app \
  --reload \
  --app-dir backend
```

---

## `No module named app`

Make sure you are inside the backend folder:

```bash
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload
```

Check whether `app/main.py` exists:

```bash
ls app
```

You may need an empty package file:

```bash
touch app/__init__.py
```

---

## Frontend Dependency Errors

From `frontend/`:

```bash
rm -rf node_modules
npm ci
```

If `package-lock.json` does not exist:

```bash
rm -rf node_modules
npm install
```

---

## Port 8000 Is Already in Use

Find the process:

```bash
lsof -i :8000
```

Stop it using its process ID:

```bash
kill PROCESS_ID
```

Run the backend on another port:

```bash
python -m uvicorn \
  app.main:app \
  --reload \
  --port 8001
```

Update `frontend/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8001
```

---

## Port 5173 Is Already in Use

Run Vite using another port:

```bash
npm run dev -- --port 5174
```

You may need to add the new origin to the backend configuration:

```env
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174
```

---

## MPS Reports `False`

Run:

```bash
python -c "
import platform
import torch

print('Machine:', platform.machine())
print('macOS:', platform.mac_ver())
print('PyTorch:', torch.__version__)
print('MPS built:', torch.backends.mps.is_built())
print('MPS available:', torch.backends.mps.is_available())
"
```

Possible reasons include:

* The Mac uses an Intel processor
* The macOS version is unsupported
* PyTorch was installed using a different Python
* The current PyTorch build does not include MPS support

The project can still run using:

```python
device = torch.device("cpu")
```

---

# 22. Daily Development Workflow

## Terminal 1 — Backend

```bash
cd /path/to/MimisGarden/backend
source .venv/bin/activate

python -m uvicorn \
  app.main:app \
  --reload
```

## Terminal 2 — Frontend

```bash
cd /path/to/MimisGarden/frontend
npm run dev
```

## Terminal 3 — Tests and Git

```bash
cd /path/to/MimisGarden

backend/.venv/bin/python \
  -m pytest \
  backend/tests \
  -v

git status
```

---

# 23. Final Verification Checklist

Run these commands from the main project folder:

```bash
test -x backend/.venv/bin/python \
  && echo "Python environment: OK"

backend/.venv/bin/python -c \
"import fastapi, sqlalchemy, PIL, numpy, sklearn, torch, torchvision; print('Backend packages: OK')"

test -f frontend/package.json \
  && echo "Frontend package file: OK"

test -d frontend/node_modules \
  && echo "Frontend dependencies: OK"

test -f .vscode/settings.json \
  && echo "VS Code settings: OK"

test -f backend/.env \
  && echo "Backend environment file: OK"

test -f frontend/.env \
  && echo "Frontend environment file: OK"
```

Verify MPS separately:

```bash
backend/.venv/bin/python -c \
"import torch; print('MPS built:', torch.backends.mps.is_built()); print('MPS available:', torch.backends.mps.is_available())"
```

---

# 24. Quick Recovery Installation

Use this block when the project already exists but the Python environment or dependencies are missing.

Run it from the main `MimisGarden` folder:

```bash
rm -rf backend/.venv

python3 -m venv backend/.venv

backend/.venv/bin/python -m pip install --upgrade \
  pip \
  setuptools \
  wheel

backend/.venv/bin/python -m pip install \
  "fastapi[standard]" \
  "uvicorn[standard]" \
  sqlalchemy \
  alembic \
  pydantic \
  pydantic-settings \
  python-multipart \
  python-dotenv \
  aiofiles \
  httpx \
  requests \
  pillow \
  numpy \
  pandas \
  scipy \
  scikit-learn \
  matplotlib \
  opencv-python \
  tqdm \
  joblib \
  torch \
  torchvision \
  pytest \
  pytest-asyncio \
  pytest-cov \
  black \
  ruff \
  mypy
```

Verify the installation:

```bash
backend/.venv/bin/python -c \
"import torch; print('PyTorch:', torch.__version__); print('MPS available:', torch.backends.mps.is_available())"
```

Reload VS Code:

```text
Shift + Command + P
Developer: Reload Window
```

Select:

```text
backend/.venv/bin/python
```

---

# 25. Quick Start Commands

After the initial setup, the normal startup process is:

## Backend

```bash
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm run dev
```

## Backend documentation

```text
http://127.0.0.1:8000/docs
```

## Frontend

```text
http://localhost:5173
```
