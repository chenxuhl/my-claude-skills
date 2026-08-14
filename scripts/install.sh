#!/bin/bash
# Link skills/ into ~/.claude/skills (macOS/Linux).
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SOURCE="$SCRIPT_DIR/../skills"
SKILLS_TARGET="$HOME/.claude/skills"

[ ! -d "$SKILLS_SOURCE" ] && { echo "ERROR: skills/ not found at $SKILLS_SOURCE"; exit 1; }
[ -e "$SKILLS_TARGET" ] && rm -rf "$SKILLS_TARGET"

ln -s "$SKILLS_SOURCE" "$SKILLS_TARGET"
echo "Linked: $SKILLS_TARGET -> $SKILLS_SOURCE"
