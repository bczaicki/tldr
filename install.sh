#!/bin/sh
# Link ~/.claude/commands/tldr.md to this repo's tldr.md so edits here are live.
set -e
src="$(cd "$(dirname "$0")" && pwd)/tldr.md"
dst="$HOME/.claude/commands/tldr.md"
mkdir -p "$(dirname "$dst")"
if [ -e "$dst" ] && [ ! -L "$dst" ]; then
  mv "$dst" "$dst.bak"
  echo "backed up $dst -> $dst.bak"
fi
ln -sfn "$src" "$dst"
echo "linked $dst -> $src"
