#!/usr/bin/env bash
set -euo pipefail

HOOK_DIR=$(git rev-parse --git-dir 2>/dev/null || echo ".git")/hooks
HOOK_FILE="$HOOK_DIR/commit-msg"

mkdir -p "$HOOK_DIR"
cat > "$HOOK_FILE" <<'HOOK'
#!/usr/bin/env bash
# commit-msg hook that runs commitlint (via npx)
if command -v npx >/dev/null 2>&1; then
  npx --no-install commitlint --edit "$1" || {
    echo "Commit message does not follow Conventional Commits. See CONTRIBUTING.md" >&2
    exit 1
  }
else
  echo "npx not found; skipping commitlint hook. Install Node.js and npm to enable commit message checks." >&2
fi
HOOK

chmod +x "$HOOK_FILE"
echo "Installed commit-msg hook at $HOOK_FILE"
