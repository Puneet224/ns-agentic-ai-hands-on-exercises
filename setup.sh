#!/usr/bin/env bash
# vitalOps.ai — one-shot project bootstrap (macOS / Linux)
# Usage:  bash setup.sh
set -e

PROJECT="vitalops"

echo "==> Checking prerequisites"
python3 --version || { echo "Python 3.10+ required"; exit 1; }
git --version    || { echo "Git required"; exit 1; }

echo "==> Creating project: $PROJECT"
mkdir -p "$PROJECT"
cd "$PROJECT"

echo "==> Creating virtual environment"
python3 -m venv venv
source venv/bin/activate

echo "==> Installing packages"
pip install --upgrade pip --quiet
pip install sqlalchemy fastapi "uvicorn[standard]" httpx streamlit plotly pandas pytest
pip freeze > requirements.txt

echo "==> Creating folder skeleton"
mkdir -p sdk/vitalops api/routes dashboard demo scripts tests
touch sdk/vitalops/__init__.py api/__init__.py api/routes/__init__.py tests/__init__.py

echo "==> Writing .gitignore"
cat > .gitignore << 'GITIGNORE'
venv/
env/
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/
*.db
*.db-shm
*.db-wal
.vitalops_spool/
.env
.streamlit/secrets.toml
.vscode/
.idea/
.DS_Store
GITIGNORE

echo "==> Writing .env.example"
cat > .env.example << 'ENVFILE'
VITALOPS_API_KEY=change-me
VITALOPS_DB_URL=sqlite:///vitalops.db
VITALOPS_ENDPOINT=http://localhost:8000
ENVFILE

echo "==> Initializing git"
git init --quiet
git add -A
git commit -m "Bootstrap vitalOps.ai project" --quiet

echo ""
echo "Done. Next steps:"
echo "  1. Copy the .github folder into $(pwd)"
echo "  2. code ."
echo "  3. In VS Code terminal:  source venv/bin/activate"
echo "  4. Copilot Chat -> Claude Opus 5 -> Agent mode -> /phase-1-schema-and-api"
