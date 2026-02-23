#!/data/data/com.termux/files/usr/bin/bash

cd ~/operatoros_live_beta
source ./venv/bin/activate

echo "Stopping any running OperatorOS..."
fuser -k 5000/tcp 2>/dev/null

echo "Updating OperatorOS scripts from execution screen..."

# Rebuild web GUI
mkdir -p ./operatoros
cat > ./operatoros/web_gui.py << 'EOPY'
from flask import Flask, render_template, Response
import threading, queue, subprocess

app = Flask(__name__)
log_queue = queue.Queue()

def run_operatoros_tasks():
    steps = [
        ("Fetching user API credentials...", ["python3", "operatoros/fetch_api.py"]),
        ("Running recursive QC...", ["python3", "operatoros/recursive_qc.py"]),
        ("Generating content...", ["python3", "operatoros/content_generator.py"]),
        ("Executing sales automation...", ["python3", "operatoros/sales_automation.py"]),
    ]
    for message, cmd in steps:
        log_queue.put(message)
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                log_queue.put(line.strip())
            process.wait()
            if process.returncode != 0:
                log_queue.put(f"{message} ❌ Failed. Retrying...")
                run_operatoros_tasks()
            else:
                log_queue.put(f"{message} ✅ Done")
        except Exception as e:
            log_queue.put(f"{message} ❌ Exception: {e}. Retrying...")
            run_operatoros_tasks()
    log_queue.put("All tasks complete! 🎉")

threading.Thread(target=run_operatoros_tasks, daemon=True).start()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            msg = log_queue.get()
            yield f"data: {msg}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
EOPY

# Rebuild dashboard template
mkdir -p ./templates
cat > ./templates/index.html << 'EOT'
<!DOCTYPE html>
<html>
<head>
    <title>OperatorOS Dashboard</title>
    <style>
        body { font-family: monospace; background: #1b1b1b; color: #eee; }
        #logs { padding: 15px; border: 1px solid #555; height: 500px; overflow-y: auto; white-space: pre-wrap; }
        h1 { color: #00ff99; }
    </style>
</head>
<body>
    <h1>OperatorOS Dashboard</h1>
    <div id="logs"></div>
    <script>
        const logDiv = document.getElementById('logs');
        const evtSource = new EventSource("/stream");
        evtSource.onmessage = function(e) {
            logDiv.innerHTML += e.data + "\n";
            logDiv.scrollTop = logDiv.scrollHeight;
        };
    </script>
</body>
</html>
EOT

echo "Launching OperatorOS GUI..."
nohup python ./operatoros/web_gui.py > nohup.out 2>&1 &

# Open browser automatically
termux-open-url http://127.0.0.1:5000
echo "OperatorOS GUI is live at http://127.0.0.1:5000"
