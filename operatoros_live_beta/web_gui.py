#!/usr/bin/env python3
from flask import Flask, render_template_string, request, jsonify
import threading, time, webbrowser, socket, os, sys

app = Flask(__name__)
app.secret_key = "operatoros-dev-key"

# ------------------------
# Global state
# ------------------------
credentials = {}
capabilities = {}
workflow_state = {"status":"IDLE","message":"Waiting for credentials"}
api_status = {}
logs = []
workflow_thread = None
workflow_running = False

REQUIRED_KEYS = {
    "cap_openai": ["openai_key"],
    "cap_x_read": ["x_bearer"],
    "cap_x_user": ["x_consumer_key","x_consumer_secret","x_access_id","x_access_secret"],
    "cap_google": ["google_key"],
    "cap_reddit": ["reddit_key"],
    "cap_facebook": ["facebook_key"],
    "cap_instagram": ["instagram_key"],
    "cap_tiktok": ["tiktok_key"]
}

# ------------------------
# Routes
# ------------------------
@app.route("/")
def index():
    html = '''
<!DOCTYPE html>
<html>
<head>
<title>OperatorOS – API Keys</title>
<style>
body { font-family: Arial; margin:20px; }
button, a.button { padding:6px 12px; margin:5px; text-decoration:none; color:white; background:#007bff; border:none; border-radius:4px; cursor:pointer; }
a.button:hover { background:#0056b3; }
.log { font-family: monospace; white-space: pre-wrap; border:1px solid #ccc; padding:5px; max-height:300px; overflow-y:auto; margin-top:10px;}
.status { font-weight:bold; margin-top:10px; }
.instructions { font-size:0.9em; color:#333; margin-bottom:10px; }
</style>
<script>
async function submitCredentials() {
    const form = document.getElementById("credentialsForm");
    const data = new FormData(form);
    const res = await fetch("/intake",{method:"POST", body:data});
    const result = await res.json();
    document.getElementById("status").innerText = result.message;
    pollStatus();
}
async function pollStatus(){
    const res = await fetch("/status");
    const data = await res.json();
    document.getElementById("status").innerText = data.status + " – " + data.message;
    setTimeout(pollStatus,1000);
}
async function startWorkflow(){ await fetch("/start_workflow",{method:"POST"}); }
async function stopWorkflow(){ await fetch("/stop_workflow",{method:"POST"}); }
window.onload = pollStatus;
</script>
</head>
<body>
<h2>OperatorOS – Credentials & Capabilities</h2>
<form id="credentialsForm" onsubmit="event.preventDefault(); submitCredentials();">
<h3>Capabilities</h3>
<label><input type="checkbox" name="cap_openai"> OpenAI – LLM</label><br>
<label><input type="checkbox" name="cap_x_read"> X/Twitter – Read-only</label><br>
<label><input type="checkbox" name="cap_x_user"> X/Twitter – User actions</label><br>
<label><input type="checkbox" name="cap_google"> Google API</label><br>
<label><input type="checkbox" name="cap_reddit"> Reddit API</label><br>
<label><input type="checkbox" name="cap_facebook"> Facebook API</label><br>
<label><input type="checkbox" name="cap_instagram"> Instagram API</label><br>
<label><input type="checkbox" name="cap_tiktok"> TikTok API</label><br><br>

<h3>API Keys & Instructions</h3>

<div class="instructions">
<label>OpenAI API Key (starts with <code>sk-</code>)</label><br>
<input name="openai_key" type="password">
<a class="button" href="https://platform.openai.com/account/api-keys" target="_blank">Get OpenAI Key</a>
<ol>
<li>Go to the link above and sign in.</li>
<li>Click "Create new secret key".</li>
<li>Copy the key including <code>sk-</code> prefix.</li>
<li>Paste it in the box above.</li>
</ol>
</div>

<div class="instructions">
<label>X API Bearer Token</label><br>
<input name="x_bearer" type="password">
<a class="button" href="https://developer.twitter.com/en/portal/dashboard" target="_blank">Get X Bearer Token</a>
<ol>
<li>Create a Twitter/X developer account if you don’t have one.</li>
<li>Create a project & app.</li>
<li>Copy the Bearer Token from your app settings.</li>
<li>Paste it here.</li>
</ol>
</div>

<div class="instructions">
<label>X API Consumer Key & Secret</label><br>
<input name="x_consumer_key" type="password" placeholder="Consumer Key">
<input name="x_consumer_secret" type="password" placeholder="Consumer Secret"><br>
<label>X Access Client ID & Secret</label><br>
<input name="x_access_id" type="password" placeholder="Client ID">
<input name="x_access_secret" type="password" placeholder="Client Secret">
<ol>
<li>In your Twitter/X app settings, generate Consumer Key & Secret.</li>
<li>Generate Access Client ID & Secret if your workflow needs user-level actions.</li>
</ol>
</div>

<div class="instructions">
<label>Google API Key</label><br>
<input name="google_key" type="password">
<a class="button" href="https://console.developers.google.com/apis/credentials" target="_blank">Get Google API Key</a>
<ol>
<li>Create a project in Google Cloud Console.</li>
<li>Go to APIs & Services → Credentials.</li>
<li>Create API Key and enable relevant APIs for your workflow.</li>
<li>Copy and paste it above.</li>
</ol>
</div>

<div class="instructions">
<label>Reddit API Key</label><br>
<input name="reddit_key" type="password">
<a class="button" href="https://www.reddit.com/prefs/apps" target="_blank">Get Reddit API Key</a>
<ol>
<li>Create a Reddit account & developer app.</li>
<li>Choose "script" app type.</li>
<li>Copy client ID & secret (or key) and paste here.</li>
</ol>
</div>

<div class="instructions">
<label>Facebook API Key</label><br>
<input name="facebook_key" type="password">
<a class="button" href="https://developers.facebook.com/apps/" target="_blank">Get Facebook API Key</a>
<ol>
<li>Create a Facebook Developer account.</li>
<li>Create a new app and select the API you need.</li>
<li>Copy the app token/key and paste it above.</li>
</ol>
</div>

<div class="instructions">
<label>Instagram API Key</label><br>
<input name="instagram_key" type="password">
<a class="button" href="https://developers.facebook.com/products/instagram" target="_blank">Get Instagram Key</a>
<ol>
<li>Create a Facebook developer app with Instagram Basic Display enabled.</li>
<li>Generate Access Token.</li>
<li>Paste it above.</li>
</ol>
</div>

<div class="instructions">
<label>TikTok API Key</label><br>
<input name="tiktok_key" type="password">
<a class="button" href="https://developers.tiktok.com/" target="_blank">Get TikTok Key</a>
<ol>
<li>Create a TikTok developer account.</li>
<li>Create a new app and generate API Key.</li>
<li>Paste the key here.</li>
</ol>
</div>

<button type="submit">Save & Continue</button>
</form>
<p id="status" class="status">Initializing…</p>
</body>
</html>
    '''
    return render_template_string(html)

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
            workflow_state["status"]="ERROR"
            workflow_state["message"]=f"Missing required keys: {', '.join(missing_keys)}"
        else:
            workflow_state["status"]="KEYS_RECEIVED"
            workflow_state["message"]="All required keys collected. Ready to start workflow."
    threading.Thread(target=deferred_validation, daemon=True).start()
    return jsonify({"ok":True,"message":"Processing credentials..."})

@app.route("/status")
def status():
    return jsonify(workflow_state)

@app.route("/start_workflow", methods=["POST"])
def start_workflow():
    global workflow_thread, workflow_running
    if workflow_thread and workflow_thread.is_alive():
        return jsonify({"ok":False,"message":"Workflow already running"})
    workflow_running = True
    workflow_thread = threading.Thread(target=workflow_loop, daemon=True)
    workflow_thread.start()
    return jsonify({"ok":True,"message":"Workflow started"})

@app.route("/stop_workflow", methods=["POST"])
def stop_workflow():
    global workflow_running
    workflow_running = False
    return jsonify({"ok":True,"message":"Workflow stopping..."})

def workflow_loop():
    while workflow_running:
        logs.append(f"[{time.strftime('%H:%M:%S')}] Starting new cycle")
        for cap in capabilities:
            if capabilities[cap]:
                api_status[cap] = "Running"
                logs.append(f"[{time.strftime('%H:%M:%S')}] Processing {cap}")
                time.sleep(2)
                api_status[cap] = "Idle"
                logs.append(f"[{time.strftime('%H:%M:%S')}] Finished {cap}")
        time.sleep(1)

# ------------------------
# Auto-select free port
# ------------------------
def get_free_port(start=5000,end=5050):
    for port in range(start,end):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            try: s.bind(("0.0.0.0",port)); return port
            except OSError: continue
    return 5000

def launch_browser(port):
    time.sleep(1)
    url=f"http://127.0.0.1:{port}"
    try:
        if sys.platform.startswith("linux"):
            os.system(f"xdg-open {url} || termux-open-url {url}")
        else:
            webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")

if __name__=="__main__":
    port=get_free_port()
    threading.Thread(target=lambda: launch_browser(port), daemon=True).start()
    app.run(host="0.0.0.0",port=port,debug=True)
