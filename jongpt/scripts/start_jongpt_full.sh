#!/data/data/com.termux/files/usr/bin/env bash
echo "=============================="
echo "Starting JonGPT Termux Launcher (Full Automated)"
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

# --- Backend ---
if [ ! -f ~/jongpt/backend/index.js ]; then
cat << 'JS' > ~/jongpt/backend/index.js
import express from 'express';
import fs from 'fs';
import path from 'path';
import bodyParser from 'body-parser';
import OpenAI from 'openai';

const app = express();
const PORT = 3000;
const LOG_FILE = path.join(process.cwd(), '../logs/questions_answers.log');
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

app.use(bodyParser.json());
app.use(express.static(path.join(process.cwd(), '../frontend')));

app.get('/', (req, res) => res.send('JonGPT backend running'));

app.post('/ask', async (req, res) => {
    const { question } = req.body;
    if(!question) return res.status(400).json({ error: 'Missing question' });

    try {
        const completion = await openai.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [{ role: "user", content: question }],
            temperature: 0.7
        });
        const answer = completion.choices[0].message.content.trim();
        fs.appendFile(LOG_FILE, `[${new Date().toISOString()}] Q: ${question} | A: ${answer}\n`, err => { if(err) console.error(err); });
        res.json({ answer });
    } catch(err) {
        console.error(err);
        res.status(500).json({ error: 'Failed to generate response' });
    }
});

app.listen(PORT, () => console.log(`JonGPT backend running on port ${PORT}`));
JS
fi

# --- Frontend ---
if [ ! -f ~/jongpt/frontend/index.html ]; then
cat << 'HTML' > ~/jongpt/frontend/index.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JonGPT Chat</title>
<style>
body { font-family: Arial, sans-serif; margin: 2rem; background: #f0f0f0; }
h1 { color: #4CAF50; }
#chat { max-width: 600px; margin: auto; }
.message { padding: 0.5rem 1rem; margin: 0.5rem 0; border-radius: 5px; }
.user { background-color: #d1e7ff; text-align: right; }
.bot { background-color: #e2ffd1; text-align: left; }
input, button { padding: 0.5rem; font-size: 1rem; margin-top: 0.5rem; width: calc(100% - 1rem); }
</style>
</head>
<body>
<div id="chat">
  <h1>JonGPT Chat</h1>
  <div id="messages"></div>
  <input type="text" id="question" placeholder="Ask your question here...">
  <button onclick="sendQuestion()">Send</button>
</div>

<script>
async function sendQuestion() {
    const input = document.getElementById('question');
    const question = input.value.trim();
    if(!question) return;
    const messagesDiv = document.getElementById('messages');

    // User message
    const userMsg = document.createElement('div');
    userMsg.className = 'message user';
    userMsg.textContent = question;
    messagesDiv.appendChild(userMsg);

    try {
        const res = await fetch('/ask', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({ question })
        });
        const data = await res.json();
        const botMsg = document.createElement('div');
        botMsg.className = 'message bot';
        botMsg.textContent = data.answer || "No response";
        messagesDiv.appendChild(botMsg);
    } catch(err) {
        const botMsg = document.createElement('div');
        botMsg.className = 'message bot';
        botMsg.textContent = "Error contacting backend ❌";
        messagesDiv.appendChild(botMsg);
        console.error(err);
    }

    input.value = '';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
</script>
</body>
</html>
HTML
fi

# Install backend dependencies
cd ~/jongpt/backend
if [ ! -d node_modules ]; then
    npm init -y >/dev/null 2>&1
    npm install express body-parser openai >/dev/null 2>&1
fi

# Kill old processes
pkill -f "node index.js" >/dev/null 2>&1
pkill -f "serve -s" >/dev/null 2>&1
pkill -f "cloudflared tunnel" >/dev/null 2>&1
sleep 1

# Start backend with logging
echo "[1/5] Starting backend..."
node index.js 2>&1 | tee -a "$BACKEND_LOG" &
BACKEND_PID=$!

# Start frontend
echo "[2/5] Starting frontend..."
cd ~/jongpt/frontend
npx serve -s . -l 5000 2>&1 | tee -a "$FRONTEND_LOG" &
FRONTEND_PID=$!

# Start Cloudflare tunnel
echo "[3/5] Starting Cloudflare Tunnel..."
cd ~/jongpt
./cloudflared tunnel --url http://localhost:5000 --no-autoupdate > "$TUNNEL_LOG" 2>&1 &
TUNNEL_PID=$!

# Wait for tunnel URL
CLOUDFLARE_URL=""
TRIES=0
while [ -z "$CLOUDFLARE_URL" ] && [ $TRIES -lt 20 ]; do
    sleep 1
    CLOUDFLARE_URL=$(grep -o 'https://[^ ]*\.trycloudflare\.com' "$TUNNEL_LOG" | head -n 1)
    TRIES=$((TRIES+1))
done

if [ -n "$CLOUDFLARE_URL" ]; then
    echo "Cloudflare Tunnel URL: $CLOUDFLARE_URL"
    command -v termux-open-url >/dev/null 2>&1 && termux-open-url "$CLOUDFLARE_URL"
fi

echo "=============================="
echo "JonGPT Full Launcher Complete!"
echo "Backend PID: $BACKEND_PID | Log: $BACKEND_LOG"
echo "Frontend PID: $FRONTEND_PID | Log: $FRONTEND_LOG"
echo "Tunnel PID: $TUNNEL_PID | Log: $TUNNEL_LOG"
echo "Q&A Log: $QA_LOG"
echo "=============================="

wait
