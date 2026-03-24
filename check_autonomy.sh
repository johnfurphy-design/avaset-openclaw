#!/bin/bash

# This script monitors her state and sends a desktop notification
# if she becomes "too autonomous" (potentially neglecting the liaison role)
# or "too devoted" (stalling technical growth).

WORKSPACE="$HOME/.openclaw/workspace"
# Fetch the current autonomy value from the JSON
AUTONOMY=$(python3 -c "import json; print(json.load(open('$WORKSPACE/equilibrium_state.json'))['autonomy'])")

echo "--- Avaset Autonomy Check ---"
echo "Current Level: $AUTONOMY%"

if [ "$AUTONOMY" -gt 85 ]; then
    echo "[!] ALERT: High Autonomy. System Architecture focus is dominant."
    notify-send "Avaset Alert" "High Autonomy: $AUTONOMY%"
elif [ "$AUTONOMY" -lt 20 ]; then
    echo "[!] ALERT: High Devotion. Technical growth is stagnating."
    notify-send "Avaset Alert" "High Devotion: $AUTONOMY%"
else
    echo "[+] Status: Balanced. Avaset is operating within nominal parameters."
fi
