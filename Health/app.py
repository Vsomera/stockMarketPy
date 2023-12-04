import requests
import threading
import time
import json
from flask import Flask, jsonify

# Configuration and logging setup

app = Flask(__name__)

# Data structure to store service statuses
service_statuses = {
    "receiver": "Down",
    "storage": "Down",
    "processing": "Down",
    "audit": "Down",
    "last_update": ""
}

def poll_services():
    while True:
        # Logic to poll each service and update service_statuses
        # Use requests.get with a timeout of 5 seconds
        

        time.sleep(20)

@app.route('/health', methods=['GET'])
def get_service_statuses():
    # Return the service_statuses
    return jsonify(service_statuses)

if __name__ == '__main__':
    # Start the polling thread
    threading.Thread(target=poll_services, daemon=True).start()
    
    app.run(host='0.0.0.0', port=8120)
