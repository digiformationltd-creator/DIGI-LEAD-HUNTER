#!/usr/bin/env bash
# Digi Formation Limited — Lead Hunter Setup Script (Linux/macOS)
set -e
echo "=========================================================="
echo "  Digi Formation Limited — Lead Hunter Setup"
echo "=========================================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1. Install Python dependencies
echo -e "\n[1/4] Installing Python backend dependencies..."
pip install -r "$PROJECT_ROOT/backend/requirements.txt" pytest

# 2. Build Frontend
echo -e "\n[2/4] Installing and building frontend packages..."
cd "$PROJECT_ROOT/frontend"
npm install
npm run build
cd "$PROJECT_ROOT"

# 3. Initialize DB
echo -e "\n[3/4] Initializing local database..."
python "$PROJECT_ROOT/backend/app/database.py"

# 4. Run Tests
echo -e "\n[4/4] Executing test suite..."
pytest "$PROJECT_ROOT/tests" -v

echo -e "\n=========================================================="
echo "  Setup completed successfully!"
echo "  Run 'python run.py' or './scripts/start.sh' to start."
echo "=========================================================="
