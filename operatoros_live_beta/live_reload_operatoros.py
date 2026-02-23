import os
import webbrowser
from flask import Flask, render_template, request, jsonify
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

# ---- Flask GUI Setup ----
app = Flask(__name__)

# Global state placeholder for OperatorOS modules
operatoros_state = {
    "status": "idle",
    "logs": []
}

@app.route('/')
def index():
    logs_html = "<br>".join(operatoros_state["logs"][-20:])  # last 20 logs
    return f"""
    <h1>OperatorOS Dashboard</h1>
    <p>Status: {operatoros_state['status']}</p>
    <h3>Logs:</h3>
    <p>{logs_html}</p>
    <button onclick="fetch('/run_task').then(r=>r.text()).then(alert)">Run Demo Task</button>
    """

@app.route('/run_task')
def run_task():
    operatoros_state["status"] = "running demo task"
    operatoros_state["logs"].append("Started demo task...")
    # Example: just sleep and log
    time.sleep(2)
    operatoros_state["logs"].append("Demo task finished!")
    operatoros_state["status"] = "idle"
    return "Demo task completed!"

# ---- Live-reload Handler ----
class ReloadHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            operatoros_state["logs"].append(f"Detected change in {event.src_path}, restarting GUI...")
            os._exit(3)  # Crash/restart signal

def start_watchdog(path="."):
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# ---- Launch browser automatically ----
def launch_browser():
    time.sleep(1)  # give server a sec
    try:
        webbrowser.open("http://127.0.0.1:5000")
    except:
        operatoros_state["logs"].append("Could not open browser automatically.")

# ---- Main Execution ----
if __name__ == "__main__":
    Thread(target=start_watchdog, args=(".",), daemon=True).start()
    Thread(target=launch_browser, daemon=True).start()
    run_flask()
