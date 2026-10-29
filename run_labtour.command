#!/bin/zsh
# Launch correct game: Cyberball_2084.
cd "/Users/macbook/projects/hus/labtour2026/Cyberball_2084" || exit 1
PY="/opt/homebrew/Caskroom/miniforge/base/envs/labtour-pong/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "Conda Python missing at: $PY"
  echo "Activate labtour-pong or update this launcher."
  read -k 1 "?Press a key to close..."
  exit 1
fi
echo "Starting Cyberball_2084 - HUS Lab Tour 2026"
"$PY" main.py
