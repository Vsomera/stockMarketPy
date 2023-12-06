import requests
import threading
import time
from flask import Flask, jsonify
from flask_cors import CORS
import yaml

# Configuration and logging setup

app = Flask(__name__)
CORS(app) 

# Data structure to store service statuses
service_statuses = {
    "receiver": "Down",
    "storage": "Down",
    "processing": "Down",
    "audit": "Down",
    "last_update": ""
}

with open("./app_conf.yml", 'r') as f:
    app_config = yaml.safe_load(f.read())

def poll_services():
    while True:
        for service_name, service_info in app_config['service'].items():
            try:
                response = requests.get(service_info['url'], timeout=5)
                # Update the status based on the response code
                service_statuses[service_name] = "Up" if response.status_code == 200 else "Down"
            except requests.RequestException:
                service_statuses[service_name] = "Down"

        # Update last_update time
        service_statuses["last_update"] = time.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(20)

@app.route('/health', methods=['GET'])
def get_service_statuses():
    # Return the service_statuses
    return jsonify(service_statuses)

if __name__ == '__main__':
    # Start the polling thread
    threading.Thread(target=poll_services, daemon=True).start()
    app.run(host='0.0.0.0', port=8120)
