#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
VENV_DIR="$BACKEND_DIR/.venv"

echo "========================================"
echo " Mimi's PlantHealth Ops macOS setup"
echo "========================================"
echo "Project root: $PROJECT_ROOT"

# --------------------------------------------------
# Verify project folders
# --------------------------------------------------

if [[ ! -d "$BACKEND_DIR" ]]; then
    echo "ERROR: backend/ folder was not found."
    echo "Open the MimisGarden root folder in VS Code and run this again."
    exit 1
fi

if [[ ! -d "$FRONTEND_DIR" ]]; then
    echo "ERROR: frontend/ folder was not found."
    echo "Open the MimisGarden root folder in VS Code and run this again."
    exit 1
fi

# --------------------------------------------------
# Verify required programs
# --------------------------------------------------

for command in python3 node npm git; do
    if ! command -v "$command" >/dev/null 2>&1; then
        echo "ERROR: $command is not installed or not available in PATH."
        exit 1
    fi
done

echo ""
echo "Python: $(python3 --version)"
echo "Node: $(node --version)"
echo "npm: $(npm --version)"
echo "Git: $(git --version)"

# --------------------------------------------------
# Backend virtual environment
# --------------------------------------------------

echo ""
echo "Creating backend Python environment..."

cd "$BACKEND_DIR"

if [[ ! -d "$VENV_DIR" ]]; then
    python3 -m venv "$VENV_DIR"
else
    echo "Existing backend/.venv detected."
fi

source "$VENV_DIR/bin/activate"

python -m pip install --upgrade \
    pip \
    setuptools \
    wheel

# --------------------------------------------------
# Backend dependencies
# --------------------------------------------------

echo ""
echo "Installing backend dependencies..."

if [[ -f requirements.txt ]]; then
    echo "Using backend/requirements.txt"
    python -m pip install -r requirements.txt
elif [[ -f pyproject.toml ]]; then
    echo "Using backend/pyproject.toml"
    python -m pip install -e .
else
    echo "No requirements file detected."
    echo "Installing Mimi's Garden backend dependencies directly."

    python -m pip install \
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
        opencv-python \
        scikit-learn \
        pandas \
        joblib \
        torch \
        torchvision \
        pytest \
        pytest-asyncio \
        pytest-cov

    python -m pip freeze > requirements.txt
    echo "Created backend/requirements.txt"
fi

# --------------------------------------------------
# Storage directories
# --------------------------------------------------

echo ""
echo "Creating storage directories..."

mkdir -p \
    "$BACKEND_DIR/storage/uploaded_images" \
    "$BACKEND_DIR/storage/models" \
    "$BACKEND_DIR/logs"

touch "$BACKEND_DIR/storage/uploaded_images/.gitkeep"
touch "$BACKEND_DIR/storage/models/.gitkeep"
touch "$BACKEND_DIR/logs/.gitkeep"

# --------------------------------------------------
# Backend environment variables
# --------------------------------------------------

if [[ ! -f "$BACKEND_DIR/.env" ]]; then
    cat > "$BACKEND_DIR/.env" <<'ENV'
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
ENV

    echo "Created backend/.env"
else
    echo "Existing backend/.env preserved."
fi

# --------------------------------------------------
# Frontend installation
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

# Install project packages only when they are missing.

npm list axios >/dev/null 2>&1 || npm install axios
npm list animejs >/dev/null 2>&1 || npm install animejs
npm list @rive-app/react-canvas >/dev/null 2>&1 || \
    npm install @rive-app/react-canvas

# --------------------------------------------------
# Frontend environment variables
# --------------------------------------------------

if [[ ! -f "$FRONTEND_DIR/.env" ]]; then
    cat > "$FRONTEND_DIR/.env" <<'ENV'
VITE_API_BASE_URL=http://127.0.0.1:8000
ENV

    echo "Created frontend/.env"
else
    echo "Existing frontend/.env preserved."
fi

# --------------------------------------------------
# VS Code configuration
# --------------------------------------------------

echo ""
echo "Creating VS Code workspace settings..."

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
        "editor.formatOnSave": true
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
        "**/.mypy_cache": true
    }
}
JSON

cat > "$PROJECT_ROOT/.vscode/extensions.json" <<'JSON'
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
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

# --------------------------------------------------
# VS Code launch configurations
# --------------------------------------------------

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
            "label": "Run Backend",
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
            "label": "Run Frontend",
            "type": "npm",
            "script": "dev",
            "path": "frontend",
            "problemMatcher": []
        },
        {
            "label": "Run Backend Tests",
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
# Update .gitignore safely
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
add_gitignore_entry ""
add_gitignore_entry "# Environment variables"
add_gitignore_entry "backend/.env"
add_gitignore_entry "frontend/.env"
add_gitignore_entry ""
add_gitignore_entry "# Databases"
add_gitignore_entry "*.db"
add_gitignore_entry "*.sqlite"
add_gitignore_entry "*.sqlite3"
add_gitignore_entry ""
add_gitignore_entry "# Uploaded files and models"
add_gitignore_entry "backend/storage/uploaded_images/*"
add_gitignore_entry "!backend/storage/uploaded_images/.gitkeep"
add_gitignore_entry "backend/storage/models/*"
add_gitignore_entry "!backend/storage/models/.gitkeep"
add_gitignore_entry ""
add_gitignore_entry "# Frontend"
add_gitignore_entry "frontend/node_modules/"
add_gitignore_entry "frontend/dist/"
add_gitignore_entry ""
add_gitignore_entry "# macOS"
add_gitignore_entry ".DS_Store"

# --------------------------------------------------
# Verify backend imports
# --------------------------------------------------

echo ""
echo "Verifying backend installation..."

cd "$BACKEND_DIR"
source "$VENV_DIR/bin/activate"

python - <<'PYTHON'
import platform

import fastapi
import numpy
import PIL
import sqlalchemy
import torch
import torchvision

print(f"Python: {platform.python_version()}")
print(f"FastAPI: {fastapi.__version__}")
print(f"SQLAlchemy: {sqlalchemy.__version__}")
print(f"NumPy: {numpy.__version__}")
print(f"Pillow: {PIL.__version__}")
print(f"PyTorch: {torch.__version__}")
print(f"Torchvision: {torchvision.__version__}")
print(f"Apple MPS available: {torch.backends.mps.is_available()}")
PYTHON

echo ""
echo "========================================"
echo " Mimi's Garden setup complete"
echo "========================================"
echo ""
echo "Restart or reload VS Code."
echo ""
echo "Backend interpreter:"
echo "$VENV_DIR/bin/python"
echo ""
echo "Backend command:"
echo "cd backend"
echo "source .venv/bin/activate"
echo "python -m uvicorn app.main:app --reload"
echo ""
echo "Frontend command:"
echo "cd frontend"
echo "npm run dev"
