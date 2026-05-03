#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== YMOS Setup ==="

# 1. Install ymos CLI globally (available as 'ymos' on PATH)
echo ""
echo "[1/2] Installing ymos CLI ..."
cd "$REPO_DIR"
if command -v ymos &>/dev/null; then
    echo "  ↻  Updating existing ymos ..."
    uv tool install --upgrade --editable .
else
    uv tool install --editable .
fi
echo "  ✅ ymos command available globally"

# 2. Initialize runtime directories
echo ""
echo "[2/2] Initializing data directories ..."
ymos init dirs

echo ""
echo "=== Setup complete ==="
echo "Skills are in .claude/skills/ (auto-discovered by Claude Code)."
echo "Run 'ymos --help' to get started."
