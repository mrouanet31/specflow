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

echo "Installing commitlint (local dev)..."
if command -v npm >/dev/null 2>&1; then
  npm ci || npm install || true
  npm install --no-save @commitlint/config-conventional @commitlint/cli || true
  ./scripts/install-commit-msg-hook.sh || true
else
  echo "npm not found. Skipping commitlint installation and hook creation. Install Node/npm to enable commit message checks." >&2
fi

echo "Done. To verify, run: ~/.local/bin/pre-commit run --all-files" 
