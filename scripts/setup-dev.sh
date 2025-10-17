#!/usr/bin/env bash
set -euo pipefail

echo "Setting up developer environment..."

if ! command -v python >/dev/null 2>&1; then
  echo "Python not found. Please install Python 3.8+ and try again." >&2
  exit 1
fi

python -m pip install --user --upgrade pip
python -m pip install --user pre-commit

echo "Installing pre-commit hooks..."
~/.local/bin/pre-commit install || pre-commit install

echo "Done. To verify, run: ~/.local/bin/pre-commit run --all-files" 
