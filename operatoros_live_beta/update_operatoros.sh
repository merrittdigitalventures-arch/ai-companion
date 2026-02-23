#!/data/data/com.termux/files/usr/bin/bash

cd ~/operatoros_live_beta

# Activate virtual environment
source ./venv/bin/activate

# Kill any process using port 5000
fuser -k 5000/tcp 2>/dev/null

# Overwrite web_gui.py with the full OperatorOS GUI + workflow code
cat > web_gui.py << 'PYEOF'
from flask import Flask, render_template, request, jsonify
import threading, time, os, webbrowser

app = Flask(__name__)
app.secret_key = "operatoros-dev-key"

# Global state
credentials = {}
capabilities = {}
workflow_state = {"status": "IDLE", "message": "Waiting for credentials"}
api_status = {}
logs = []
workflow_thread = None
workflow_running = False

# Define required API keys per capability
REQUIRED_KEYS = {
    "cap_openai": ["openai_key"],
    "cap_x_read": ["x_bearer"],
    "cap_x_user": ["x_consumer_key","x_consumer_secret","x_access_id","x_access_secret"],
    "cap_google": ["google_key"],
    "cap_reddit": ["reddit_key"]
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/intake", methods=["POST"])
def intake():
    global credentials, capabilities
    capabilities = {key: key in request.form for key in REQUIRED_KEYS}
    for key in request.form:
        credentials[key] = request.form.get(key)

    missing_keys = []
    for cap, keys in REQUIRED_KEYS.items():
        if capabilities.get(cap):
            for k in keys:
                if not credentials.get(k):
                    missing_keys.append(k)

    def deferred_validation():
        if missing_keys:
            workflow_state["status"] = "ERROR"
            workflow_state["message"] = f"Missing required keys: {', '.join(missing_keys)}"
        else:
            workflow_state["status"] = "KEYS_RECEIVED"
            workflow_state["message"] = "All required keys collected. Ready to start workflow."

    threading.Thread(target=deferred_validation, daemon=True).start()
    return jsonify({"ok": True, "message": "Processing credentials..."})

@app.route("/status")
def status():
    return jsonify(workflow_state)

@app.route("/dashboard_status")
def dashboard_status():
    return jsonify({"api_status": api_status, "logs": logs})

@app.route("/start_workflow", methods=["POST"])
def start_workflow():
    global workflow_thread, workflow_running
    if workflow_thread and workflow_thread.is_alive():
        return jsonify({"ok": False, "message": "Workflow already running"})
    workflow_running = True
    workflow_thread = threading.Thread(target=workflow_loop, daemon=True)
    workflow_thread.start()
    return jsonify({"ok": True, "message": "Workflow started"})

@app.route("/stop_workflow", methods=["POST"])
def stop_workflow():
    global workflow_running
    workflow_running = False
    return jsonify({"ok": True, "message": "Workflow stopping..."})

def workflow_loop():
    while workflow_running:
        logs.append(f"[{time.strftime('%H:%M:%S')}] Starting new cycle")
        for cap in capabilities:
            if capabilities[cap]:
                api_status[cap] = "Running"
                logs.append(f"[{time.strftime('%H:%M:%S')}] Processing {cap}")
                time.sleep(2)  # placeholder for actual work
                api_status[cap] = "Idle"
                logs.append(f"[{time.strftime('%H:%M:%S')}] Finished {cap}")
        time.sleep(1)

def launch_browser():
    time.sleep(1)
    try:
        os.system("termux-open-url http://127.0.0.1:5000/dashboard")
    except:
        try:
            webbrowser.open("http://127.0.0.1:5000/dashboard")
        except Exception as e:
            print(f"Could not open browser automatically: {e}")

if __name__ == "__main__":
    threading.Thread(target=launch_browser, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True)
PYEOF

# Start the OperatorOS GUI
nohup python ./web_gui.py > nohup.out 2>&1 &

# Give Flask a second to start and try to open browser
sleep 1
termux-open-url http://127.0.0.1:5000/dashboard 2>/dev/null || python -m webbrowser http://127.0.0.1:5000/dashboard

echo "OperatorOS GUI updated and started! Access it at http://127.0.0.1:5000"
