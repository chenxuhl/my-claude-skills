#!/bin/bash
# Claude Code Skills Installation Script for macOS/Linux
# This script links or copies the skills to your Claude Code configuration

set -e

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_SOURCE="$PROJECT_ROOT/skills"

# Claude Code config path
CLAUDE_CONFIG_PATH="$HOME/.claude"
SKILLS_TARGET="$CLAUDE_CONFIG_PATH/skills"

echo "========================================"
echo "Claude Code Skills Installation"
echo "========================================"
echo ""

# Check if skills directory exists
if [ ! -d "$SKILLS_SOURCE" ]; then
    echo "ERROR: Skills directory not found at: $SKILLS_SOURCE"
    exit 1
fi

echo "Source: $SKILLS_SOURCE"
echo "Target: $SKILLS_TARGET"
echo ""

# Check if Claude config directory exists
if [ ! -d "$CLAUDE_CONFIG_PATH" ]; then
    echo "Creating Claude Code config directory..."
    mkdir -p "$CLAUDE_CONFIG_PATH"
fi

# Check if skills target already exists
if [ -e "$SKILLS_TARGET" ]; then
    if [ -L "$SKILLS_TARGET" ]; then
        echo "Existing symbolic link found."
        read -p "Remove and recreate? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm "$SKILLS_TARGET"
            echo "Removed existing link."
        else
            echo "Installation cancelled."
            exit 0
        fi
    elif [ -d "$SKILLS_TARGET/.git" ]; then
        echo "ERROR: Target is a git repository. Remove manually if needed."
        exit 1
    else
        echo "Existing directory found. This will be replaced."
        read -p "Continue? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$SKILLS_TARGET"
            echo "Removed existing directory."
        else
            echo "Installation cancelled."
            exit 0
        fi
    fi
fi

# Create symbolic link
echo ""
echo "Creating symbolic link..."
ln -s "$SKILLS_SOURCE" "$SKILLS_TARGET"
echo "SUCCESS: Symbolic link created!"

echo ""
echo "========================================"
echo "Installation complete!"
echo "========================================"
echo ""
echo "Skills are now available in Claude Code:"
for skill_dir in "$SKILLS_SOURCE"/*/; do
    skill_name="$(basename "$skill_dir")"
    skill_md="$skill_dir/skill.md"
    if [ -f "$skill_md" ]; then
        title=$(grep "^title:" "$skill_md" | sed 's/title: //; s/"//g' | xargs)
    fi
    if [ -z "$title" ]; then
        title="$skill_name"
    fi
    echo "  - $title"
done
echo ""
