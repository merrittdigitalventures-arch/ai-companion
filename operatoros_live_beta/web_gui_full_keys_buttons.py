from flask import Flask, render_template_string, request, jsonify
import threading, time, webbrowser, socket, os

app = Flask(__name__)
app.secret_key = "operatoros-dev-key"

# Global state
credentials = {}
workflow_running = False
workflow_thread = None
api_status = {}
logs = []

REQUIRED_KEYS = {
    "OpenAI": ["openai_key"],
    "X Read": ["x_bearer"],
    "X User": ["x_consumer_key","x_consumer_secret","x_access_id","x_access_secret"],
    "Google": ["google_key"],
    "Reddit": ["reddit_key"],
    "Instagram": ["instagram_key"],
    "Facebook": ["facebook_key"],
    "TikTok": ["tiktok_key"]
}

GUIDE_TEXT = {
    "openai_key": "Step 1: Go to https://platform.openai.com/account/api-keys\nStep 2: Click 'Create new secret key'\nStep 3: Copy & paste here",
    "x_bearer": "X (Twitter) Bearer Token: https://developer.twitter.com/en/docs/authentication/oauth-2.0/bearer-tokens",
    "x_consumer_key": "X Consumer Key: https://developer.twitter.com/en/portal/dashboard",
    "x_consumer_secret": "X Consumer Secret: https://developer.twitter.com/en/portal/dashboard",
    "x_access_id": "X Access Client ID: create an App in Twitter Developer Portal",
    "x_access_secret": "X Access Client Secret: create an App in Twitter Developer Portal",
    "google_key": "Google API Key: https://console.cloud.google.com/apis/credentials",
    "reddit_key": "Reddit API Key: https://www.reddit.com/prefs/apps",
    "instagram_key": "Instagram Graph API token: https://developers.facebook.com/docs/instagram-api/getting-started",
    "facebook_key": "Facebook Graph API token: https://developers.facebook.com/docs/apps/",
    "tiktok_key": "TikTok Developer token: https://developers.tiktok.com/doc/login-kit-web/"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>OperatorOS – API Credentials</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        h3 { margin-top: 20px; }
        label { display: block; margin-bottom: 5px; }
        input { width: 300px; padding: 5px; margin-bottom: 5px; }
        .instructions { font-size: 0.9em; color: #555; margin-bottom: 10px; }
        button { padding: 6px 10px; margin-left: 5px; }
    </style>
    <script>
        function openKeyGuide(url, instructions) {
            window.open(url, "_blank");
            alert(instructions);
        }
        async function submitCredentials() {
            const form = document.getElementById("credentialsForm");
            const data = new FormData(form);
            const res = await fetch("/intake", {method:"POST", body:data});
            const result = await res.json();
            document.getElementById("status").innerText = result.message;
        }
    </script>
</head>
<body>
<h2>OperatorOS – API Credentials Intake</h2>
<form id="credentialsForm" onsubmit="event.preventDefault(); submitCredentials();">
{% for cap, keys in REQUIRED_KEYS.items() %}
    <h3>{{cap}}</h3>
    {% for key in keys %}
        <label>{{key.replace('_',' ').title()}}</label>
        <input name="{{key}}" type="password" placeholder="Paste your key here">
        <button type="button" onclick="openKeyGuide('{{GUIDE_URLS[key]}}', '{{GUIDE_TEXT[key]}}')">Get Key</button>
        <div class="instructions">{{GUIDE_TEXT[key]}}</div>
    {% endfor %}
{% endfor %}
<button type="submit">Save & Continue</button>
</form>
<p id="status">Waiting for credentials...</p>
</body>
</html>
"""

GUIDE_URLS = {
    "openai_key": "https://platform.openai.com/account/api-keys",
    "x_bearer": "https://developer.twitter.com/en/docs/authentication/oauth-2.0/bearer-tokens",
    "x_consumer_key": "https://developer.twitter.com/en/portal/dashboard",
    "x_consumer_secret": "https://developer.twitter.com/en/portal/dashboard",
    "x_access_id": "https://developer.twitter.com/en/portal/dashboard",
    "x_access_secret": "https://developer.twitter.com/en/portal/dashboard",
    "google_key": "https://console.cloud.google.com/apis/credentials",
    "reddit_key": "https://www.reddit.com/prefs/apps",
    "instagram_key": "https://developers.facebook.com/docs/instagram-api/getting-started",
    "facebook_key": "https://developers.facebook.com/docs/apps/",
    "tiktok_key": "https://developers.tiktok.com/doc/login-kit-web/"
}

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, REQUIRED_KEYS=REQUIRED_KEYS, GUIDE_TEXT=GUIDE_TEXT, GUIDE_URLS=GUIDE_URLS)

@app.route("/intake", methods=["POST"])
def intake():
    global credentials
    for key in request.form:
        credentials[key] = request.form.get(key)
    missing_keys = [k for keys in REQUIRED_KEYS.values() for k in keys if not credentials.get(k)]
    if missing_keys:
        return jsonify({"ok": False, "message": f"Missing keys: {', '.join(missing_keys)}"})
    return jsonify({"ok": True, "message": "All keys received. You can now start the workflow."})

@app.route("/dashboard_status")
def dashboard_status():
    return jsonify({"api_status": api_status, "logs": logs})

@app.route("/start_workflow", methods=["POST"])
def start_workflow():
    global workflow_running, workflow_thread
    if workflow_running:
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
    global workflow_running
    while workflow_running:
        logs.append(f"[{time.strftime('%H:%M:%S')}] Starting new cycle")
        for cap in REQUIRED_KEYS.keys():
            api_status[cap] = "Running"
            logs.append(f"[{time.strftime('%H:%M:%S')}] Processing {cap}")
            time.sleep(2)
            api_status[cap] = "Idle"
            logs.append(f"[{time.strftime('%H:%M:%S')}] Finished {cap}")
        time.sleep(1)

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port

def launch_browser(url):
    time.sleep(1)
    try:
        os.system(f"termux-open-url {url}")
    except:
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Could not open browser automatically: {e}")

if __name__ == "__main__":
    port = find_free_port()
    threading.Thread(target=launch_browser, args=(f"http://127.0.0.1:{port}/",), daemon=True).start()
    app.run(host="0.0.0.0", port=port, debug=True)
