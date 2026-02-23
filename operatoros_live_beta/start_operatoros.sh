#!/data/data/com.termux/files/usr/bin/bash

echo "=== OperatorOS Boot Sequence ==="

cd ~/operatoros_live_beta || exit 1

# Activate venv
source ./venv/bin/activate

# Kill any stale Flask instances
echo "[+] Cleaning old processes..."
pkill -f web_gui.py 2>/dev/null
pkill -f flask 2>/dev/null
sleep 1

# Start Flask in background
echo "[+] Launching GUI server..."
nohup python web_gui.py > nohup.out 2>&1 &

# Wait for server to bind
sleep 3

# Auto-open browser (Termux Android)
URL="http://127.0.0.1:5000"
echo "[+] Opening browser at $URL"
termux-open-url "$URL"

echo "=== OperatorOS is LIVE ==="
echo "Logs: ~/operatoros_live_beta/nohup.out"
