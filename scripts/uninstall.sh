#!/bin/bash
# Remove the skills link from ~/.claude/skills (macOS/Linux).
set -e
TARGET="$HOME/.claude/skills"
[ -d "$TARGET/.git" ] && { echo "Refusing: target is a git repo"; exit 1; }
[ -e "$TARGET" ] && { rm -rf "$TARGET"; echo "Removed: $TARGET"; }
