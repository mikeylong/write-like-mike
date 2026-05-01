#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Install write-like-mike for Codex and/or Claude.

Usage:
  ./scripts/install.sh [--codex] [--claude] [--all] [--force]

Options:
  --codex   Install a clean Codex runtime package into the local Codex skills directory.
  --claude  Install a Claude personal skill symlink to this canonical repo.
  --all     Install both Codex and Claude targets.
  --force   Replace an existing install target.
  -h, --help

Default behavior:
  If no target flag is given, install Codex only.
EOF
}

force=0
install_codex=0
install_claude=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --codex)
      install_codex=1
      shift
      ;;
    --claude)
      install_claude=1
      shift
      ;;
    --all)
      install_codex=1
      install_claude=1
      shift
      ;;
    --force)
      force=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ "$install_codex" -eq 0 && "$install_claude" -eq 0 ]]; then
  install_codex=1
fi

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
codex_home="${CODEX_HOME:-$HOME/.codex}"
claude_home="${CLAUDE_HOME:-$HOME/.claude}"

replace_target_or_fail() {
  local label="$1"
  local target="$2"

  if [[ -e "$target" || -L "$target" ]]; then
    if [[ "$force" -eq 1 ]]; then
      rm -rf "$target"
    else
      echo "$label install target already exists: $target" >&2
      echo "Re-run with --force to replace it." >&2
      exit 1
    fi
  fi
}

install_codex_target() {
  local target="$codex_home/skills/write-like-mike"

  mkdir -p "$(dirname "$target")"
  replace_target_or_fail "Codex" "$target"
  mkdir -p "$target"

  rsync -a --delete \
    --exclude='.git/' \
    --exclude='.claude/' \
    --exclude='__pycache__/' \
    --exclude='*.pyc' \
    "$repo_root/" "$target/"

  echo "Codex installed"
  echo "  source: $repo_root"
  echo "  target: $target"
}

install_claude_target() {
  local target="$claude_home/skills/write-like-mike"

  mkdir -p "$(dirname "$target")"

  if [[ -L "$target" && "$(readlink "$target")" == "$repo_root" ]]; then
    echo "Claude already installed"
    echo "  source: $repo_root"
    echo "  target: $target"
    return
  fi

  replace_target_or_fail "Claude" "$target"
  ln -s "$repo_root" "$target"

  echo "Claude installed"
  echo "  source: $repo_root"
  echo "  target: $target"
}

if [[ "$install_codex" -eq 1 ]]; then
  install_codex_target
fi

if [[ "$install_claude" -eq 1 ]]; then
  install_claude_target
fi
