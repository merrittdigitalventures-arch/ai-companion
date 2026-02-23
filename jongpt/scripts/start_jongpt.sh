#!/data/data/com.termux/files/usr/bin/bash
echo "=============================="
echo "Starting JonGPT Termux Launcher (headless)"
echo "=============================="

# Kill old Node.js processes
pkill -f node >/dev/null 2>&1

# Start backend
echo "[1/4] Starting backend..."
cd ~/jongpt/backend
node index.js &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Start frontend
echo "[2/4] Starting frontend..."
~/jongpt/scripts/start_frontend.sh

# Wait for tunnel URL
echo "[3/4] Waiting for LocalTunnel URL..."
TUNNEL_URL=""
while [ -z "$TUNNEL_URL" ]; do
    sleep 1
    if [ -f ~/jongpt/backend/tunnel.url ]; then
        TUNNEL_URL=$(cat ~/jongpt/backend/tunnel.url)
    fi
done
echo "Public URL: $TUNNEL_URL"

# Headless, no browser
echo "[4/4] Launcher complete (headless)."
echo "Backend Public URL: $TUNNEL_URL"
echo "Frontend URL: http://localhost:5000"
echo "=============================="
