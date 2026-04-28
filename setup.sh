#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$REPO_DIR/skills"
SKILLS_DST="$HOME/.agents/skills"

echo "=== YMOS Setup ==="

# 1. Install skills to ~/.agents/skills/
echo ""
echo "[1/3] Installing skills to $SKILLS_DST ..."
mkdir -p "$SKILLS_DST"
installed=0
for skill_dir in "$SKILLS_SRC"/*/; do
    skill_name="$(basename "$skill_dir")"
    dst="$SKILLS_DST/$skill_name"
    if [ -d "$dst" ]; then
        echo "  ↻  $skill_name (updating)"
    else
        echo "  +  $skill_name"
    fi
    cp -R "$skill_dir" "$dst"
    installed=$((installed + 1))
done
echo "  ✅ $installed skills installed"

# 2. Install ymos CLI globally (available as 'ymos' on PATH)
echo ""
echo "[2/3] Installing ymos CLI ..."
cd "$REPO_DIR"
if command -v ymos &>/dev/null; then
    echo "  ↻  Updating existing ymos ..."
    uv tool install --upgrade --editable .
else
    uv tool install --editable .
fi
echo "  ✅ ymos command available globally"

# 3. Initialize runtime directories
echo ""
echo "[3/3] Initializing data directories ..."
ymos init dirs

echo ""
echo "=== Setup complete ==="
echo "Run 'ymos --help' to get started."
