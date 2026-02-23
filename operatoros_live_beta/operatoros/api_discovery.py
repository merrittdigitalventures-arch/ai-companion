from flask import Blueprint, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import threading
import json
import time

api_discovery_bp = Blueprint('api_discovery', __name__, template_folder='templates')

discovered_apis = []

def launch_headless_browser(username, password, login_url):
    global discovered_apis

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.binary_location = "/data/data/com.termux/files/usr/bin/chromium"

    driver = webdriver.Chrome(options=options)
    driver.get(login_url)

    try:
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
    except Exception as e:
        print("Login automation failed:", e)

    time.sleep(5)

    for entry in driver.get_log('performance'):
        try:
            message = json.loads(entry['message'])['message']
            if message['method'] == 'Network.requestWillBeSent':
                url = message['params']['request']['url']
                if url.startswith("http") and url not in discovered_apis:
                    discovered_apis.append(url)
        except Exception:
            continue

    driver.quit()

@api_discovery_bp.route('/api_discovery', methods=['GET', 'POST'])
def api_discovery():
    global discovered_apis
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        login_url = request.form.get('login_url')

        thread = threading.Thread(target=launch_headless_browser, args=(username, password, login_url))
        thread.start()

        return jsonify({"status": "started", "message": "API discovery started. Refresh page after a few seconds."})

    return render_template('api_discovery.html', apis=discovered_apis)
