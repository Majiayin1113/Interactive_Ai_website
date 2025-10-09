#!/usr/bin/env bash
set -euo pipefail

BASE_DIR=${1:-"F:/PolyU/Sem1/5913Programming"}
VENV_NAME=${2:-"$BASE_DIR/.venv"}
PYTHON=${3:-python3}

echo "Creating virtual environment '$VENV_NAME' using $PYTHON"
$PYTHON -m venv "$VENV_NAME"
echo "Activating and installing requirements"
source "$VENV_NAME/bin/activate"
python -m pip install --upgrade pip
pip install -r requirements.txt
echo "Done. Activate with: source $VENV_NAME/bin/activate"
