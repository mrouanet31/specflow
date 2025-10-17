#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMPORTER="$SCRIPT_DIR/github_issue_importer.py"

usage() {
  cat <<EOF
Usage: run_import.sh owner/repo path/to/backlog.csv [--create-labels] [--label-estimate] [--concurrency N]

This helper validates GITHUB_TOKEN, runs a dry-run first and asks confirmation before doing the real import.
EOF
}

if [ "$#" -lt 2 ]; then
  usage
  exit 1
fi

REPO="$1"
CSV_PATH="$2"
shift 2
EXTRA_ARGS="$@"

if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "GITHUB_TOKEN not set. Please export your token (do NOT commit it)."
  exit 2
fi

echo "Running dry-run..."
python3 "$IMPORTER" --dry-run "$REPO" "$CSV_PATH" $EXTRA_ARGS

read -p "Dry-run complete. Proceed with real import? [y/N] " answer
case "$answer" in
  y|Y)
    echo "Running real import..."
    python3 "$IMPORTER" "$REPO" "$CSV_PATH" $EXTRA_ARGS
    ;;
  *)
    echo "Aborted by user. No changes made."
    exit 0
    ;;
esac
