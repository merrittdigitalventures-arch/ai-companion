#!/bin/bash
# JonGPT Termux Launcher (Backend + LocalTunnel + Logging + auto ai-plugin.json)

# 0️⃣ Stop old Node processes
echo "Stopping old Node.js processes..."
pkill -f "node" || true

# 1️⃣ Start backend
echo "[1/4] Starting JonGPT backend..."
cd ~/jongpt/backend || exit 1

mkdir -p logs

nohup node index.js >> logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

sleep 3

# 2️⃣ Start LocalTunnel
echo "[2/4] Starting LocalTunnel..."
nohup npx localtunnel --port 3000 >> logs/tunnel.log 2>&1 &
TUNNEL_PID=$!

sleep 5

# 3️⃣ Get public URL from LocalTunnel
PUBLIC_URL=$(grep -o "https://.*\.loca\.lt" logs/tunnel.log | head -n1)

if [ -z "$PUBLIC_URL" ]; then
    echo "Error: Could not determine LocalTunnel URL. Check logs/tunnel.log"
else
    echo "LocalTunnel Public URL: $PUBLIC_URL"

    # 4️⃣ Auto-generate ai-plugin.json
    cat <<JSON_EOF > ~/jongpt/backend/ai-plugin.json
{
  "name": "JonGPT",
  "description": "ChatGPT plugin for JonGPT",
  "auth": {
    "type": "none"
  },
  "api": {
    "type": "openapi",
    "url": "$PUBLIC_URL/openapi.json",
    "is_user_authenticated": true
  },
  "logo_url": "https://example.com/logo.png",
  "contact_email": "you@example.com",
  "legal_info_url": "https://example.com/legal"
}
JSON_EOF

    echo "ai-plugin.json updated with current LocalTunnel URL."
fi

echo "[4/4] JonGPT launcher ready."
echo "Backend PID: $BACKEND_PID, Tunnel PID: $TUNNEL_PID"
echo "Check logs in ~/jongpt/backend/logs for details."
