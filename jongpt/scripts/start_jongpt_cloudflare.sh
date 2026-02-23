#!/data/data/com.termux/files/usr/bin/env bash
echo "=============================="
echo "Starting JonGPT Termux Launcher (Cloudflare Tunnel, Auto-Restart, Logging)"
echo "=============================="

# Create required directories
mkdir -p ~/jongpt/logs
mkdir -p ~/jongpt/backend
mkdir -p ~/jongpt/frontend

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKEND_LOG=~/jongpt/logs/backend_$TIMESTAMP.log
FRONTEND_LOG=~/jongpt/logs/frontend_$TIMESTAMP.log
TUNNEL_LOG=~/jongpt/logs/cloudflared_$TIMESTAMP.log
QA_LOG=~/jongpt/logs/questions_answers_$TIMESTAMP.log

# Create placeholder frontend if missing
if [ ! -f ~/jongpt/frontend/index.html ]; then
cat << 'HTML' > ~/jongpt/frontend/index.html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>JonGPT Frontend</title>
</head>
<body>
  <h1>JonGPT Frontend</h1>
  <p>Ask your questions through the bot API.</p>
</body>
</html>
HTML
fi

# Create placeholder backend if missing
if [ ! -f ~/jongpt/backend/index.js ]; then
cat << 'JS' > ~/jongpt/backend/index.js
import express from 'express';
import fs from 'fs';
import path from 'path';
import bodyParser from 'body-parser';

const app = express();
const PORT = 3000;
const LOG_FILE = path.join(process.cwd(), '../logs/questions_answers.log');

app.use(bodyParser.json());

// Root route
app.get('/', (req, res) => res.send('JonGPT Backend is running'));

// Endpoint for questions
app.post('/ask', (req, res) => {
    const { question, response } = req.body;
    if(question && response){
        const logLine = `[${new Date().toISOString()}] Q: ${question} | A: ${response}\n`;
        fs.appendFile(LOG_FILE, logLine, err => {
            if(err) console.error('Failed to log Q&A:', err);
        });
        res.json({ status: 'logged' });
    } else {
        res.status(400).json({ error: 'Missing question or response' });
    }
});

app.listen(PORT, () => {
    console.log(`JonGPT backend running on port ${PORT}`);
});
JS
fi

# Install backend dependencies if missing
cd ~/jongpt/backend
if [ ! -d node_modules ]; then
    npm init -y >/dev/null 2>&1
    npm install express body-parser >/dev/null 2>&1
fi

# 0️⃣ Kill old processes to prevent conflicts
echo "[0/6] Killing old backend, frontend, and cloudflared processes..."
pkill -f "node index.js" >/dev/null 2>&1
pkill -f "serve -s" >/dev/null 2>&1
pkill -f "cloudflared tunnel" >/dev/null 2>&1
sleep 1

# Function to start backend with auto-restart
start_backend() {
    while true; do
        echo "[BACKEND] Starting..." | tee -a "$BACKEND_LOG"
        cd ~/jongpt/backend
        node index.js 2>&1 | tee -a "$BACKEND_LOG"
        echo "[BACKEND] Crashed or exited. Restarting in 2s..." | tee -a "$BACKEND_LOG"
        sleep 2
    done
}

# Function to start frontend with auto-restart
start_frontend() {
    while true; do
        echo "[FRONTEND] Starting..." | tee -a "$FRONTEND_LOG"
        cd ~/jongpt/frontend
        npx serve -s . -l 5000 2>&1 | tee -a "$FRONTEND_LOG"
        echo "[FRONTEND] Crashed or exited. Restarting in 2s..." | tee -a "$FRONTEND_LOG"
        sleep 2
    done
}

# 1️⃣ Start backend in background
echo "[1/6] Starting backend with auto-restart..."
start_backend &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# 2️⃣ Start frontend in background
echo "[2/6] Starting frontend with auto-restart..."
start_frontend &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# 3️⃣ Start Cloudflare Tunnel
echo "[3/6] Starting Cloudflare Tunnel..."
cd ~/jongpt
./cloudflared tunnel --url http://localhost:5000 --no-autoupdate > "$TUNNEL_LOG" 2>&1 &
TUNNEL_PID=$!

#  ⏳ Wait for tunnel to initialize and grab public URL
CLOUDFLARE_URL=""
TRIES=0
while [ -z "$CLOUDFLARE_URL" ] && [ $TRIES -lt 20 ]; do
    sleep 1
    CLOUDFLARE_URL=$(grep -o 'https://[^ ]*\.trycloudflare\.com' "$TUNNEL_LOG" | head -n 1)
    TRIES=$((TRIES+1))
done

if [ -z "$CLOUDFLARE_URL" ]; then
    echo "Failed to detect Cloudflare URL. Check $TUNNEL_LOG for details."
else
    echo "Cloudflare Tunnel Public URL: $CLOUDFLARE_URL"

    # Copy URL to clipboard if Termux API available
    if command -v termux-clipboard-set >/dev/null 2>&1; then
        termux-clipboard-set "$CLOUDFLARE_URL"
        echo "URL copied to clipboard!"
    fi

    # Open browser automatically if Termux API available
    if command -v termux-open-url >/dev/null 2>&1; then
        echo "[4/6] Opening browser..."
        termux-open-url "$CLOUDFLARE_URL"
    fi
fi

echo "=============================="
echo "JonGPT Launcher Complete!"
echo "Backend PID: $BACKEND_PID | Log: $BACKEND_LOG"
echo "Frontend PID: $FRONTEND_PID | Log: $FRONTEND_LOG"
echo "Cloudflare Tunnel PID: $TUNNEL_PID | Log: $TUNNEL_LOG"
echo "Q&A Log: $QA_LOG"
echo "=============================="

# 5️⃣ Keep the script alive to monitor processes
wait
