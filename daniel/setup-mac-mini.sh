#!/bin/bash
# ===========================================
# Daniel — setup pro Mac Mini
# Spusť tento skript na Mac Mini v práci.
# Soubor se automaticky synchronizoval přes iCloud.
# ===========================================

set -e

echo "=== Daniel setup pro Mac Mini ==="
echo ""

# 1. Kontrola — iCloud musí mít XLAB/Daniel
ICLOUD_DIR=~/Library/Mobile\ Documents/com~apple~CloudDocs/XLAB/Daniel
if [ ! -d "$ICLOUD_DIR" ]; then
    echo "CHYBA: iCloud ještě nesynchronizoval ~/Library/Mobile Documents/com~apple~CloudDocs/XLAB/Daniel/"
    echo "Otevři Finder, jdi do iCloud Drive > XLAB > Daniel a počkej, až se stáhne."
    exit 1
fi
echo "✓ iCloud složka nalezena"

# 2. Symlink ~/Daniel/
if [ -L ~/Daniel ]; then
    echo "✓ ~/Daniel/ symlink už existuje"
elif [ -d ~/Daniel ]; then
    echo "CHYBA: ~/Daniel/ existuje jako složka (ne symlink). Přejmenuj ji nebo smaž."
    exit 1
else
    ln -s "$ICLOUD_DIR" ~/Daniel
    echo "✓ Vytvořen symlink ~/Daniel/ → iCloud"
fi

# 3. Claude Code CLI
if command -v claude &> /dev/null; then
    echo "✓ Claude Code CLI je nainstalovaný"
else
    echo "Instaluji Claude Code CLI..."
    npm install -g @anthropic-ai/claude-code
    echo "✓ Claude Code CLI nainstalovaný"
fi

# 4. ~/.claude/ adresář
mkdir -p ~/.claude

# 5. Symlink CLAUDE.md
if [ -L ~/.claude/CLAUDE.md ]; then
    echo "✓ CLAUDE.md symlink už existuje"
else
    [ -f ~/.claude/CLAUDE.md ] && mv ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak
    ln -s "$ICLOUD_DIR/.claude-sync/CLAUDE.md" ~/.claude/CLAUDE.md
    echo "✓ CLAUDE.md → iCloud"
fi

# 6. Symlink commands/
if [ -L ~/.claude/commands ]; then
    echo "✓ commands/ symlink už existuje"
else
    [ -d ~/.claude/commands ] && mv ~/.claude/commands ~/.claude/commands.bak
    ln -s "$ICLOUD_DIR/.claude-sync/commands" ~/.claude/commands
    echo "✓ commands/ → iCloud"
fi

# 7. Memory — potřebujeme zjistit project path pro tento Mac
# Claude Code používá absolutní cestu k working directory jako klíč
RESOLVED_PATH=$(cd ~/Daniel && pwd -P)
# Nahradí / za - a odstraní první -
PROJECT_KEY=$(echo "$RESOLVED_PATH" | sed 's|/|-|g')
MEMORY_DIR=~/.claude/projects/$PROJECT_KEY

mkdir -p "$MEMORY_DIR"
if [ -L "$MEMORY_DIR/memory" ]; then
    echo "✓ memory symlink už existuje"
else
    [ -d "$MEMORY_DIR/memory" ] && rmdir "$MEMORY_DIR/memory" 2>/dev/null
    ln -s "$ICLOUD_DIR/.claude-sync/memory" "$MEMORY_DIR/memory"
    echo "✓ memory → iCloud (project key: $PROJECT_KEY)"
fi

# 8. Symlink .mcp.json (MS 365 — Outlook, Teams, kalendář)
if [ -L ~/.mcp.json ]; then
    echo "✓ .mcp.json symlink už existuje"
else
    [ -f ~/.mcp.json ] && mv ~/.mcp.json ~/.mcp.json.bak
    ln -s "$ICLOUD_DIR/.claude-sync/mcp.json" ~/.mcp.json
    echo "✓ .mcp.json → iCloud"
fi

# 9. Symlink projects dir (sessions sdílené mezi Macy)
SYMLINK_PROJECT=~/.claude/projects/-Users-machintoshhd-Daniel
if [ -L "$SYMLINK_PROJECT" ]; then
    echo "✓ projects symlink už existuje"
else
    [ -d "$SYMLINK_PROJECT" ] && rm -rf "$SYMLINK_PROJECT"
    ln -s "$MEMORY_DIR" "$SYMLINK_PROJECT"
    echo "✓ projects symlink → sessions sdílené"
fi

echo ""
echo "=== Hotovo! ==="
echo ""
echo "Spusť Daniela:"
echo "  cd ~/Daniel && claude"
echo ""
