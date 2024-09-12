from flask import Flask, request, jsonify, redirect, Response
import requests
import json
import os
import threading
import time
from urllib.parse import urlparse

app = Flask(__name__)

config = {}
config_path = 'routes.json'
last_modified_time = None

def load_config():
    global config, last_modified_time
    with open(config_path) as f:
        config = json.load(f)
    last_modified_time = os.path.getmtime(config_path)
    print("Configuration loaded")
    print(config)

def watch_config():
    global last_modified_time
    while True:
        try:
            current_modified_time = os.path.getmtime(config_path)
            if current_modified_time != last_modified_time:
                print("Configuration file changed. Reloading...")
                load_config()
        except Exception as e:
            print(f"Error watching config file: {e}")
        time.sleep(5)

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def proxy(path):

    # Handle blank requests from frontend proxy congifuration
    if path == '':
        # Handle the root path explicitly
        return jsonify({"message": "Proxy is running"}), 200
    
    print(f"Received request for raw path: {request.path}")
    if request.method == 'POST':
        print(f"POST body: {request.get_json()}")
    print(f"Query string: {request.query_string.decode('utf-8')}")
    print(f"Processed path: /{path}")
    
    # Extract just the path without query parameters
    parsed_url = urlparse(request.full_path)
    clean_path = parsed_url.path.strip("/")
    print(f"Cleaned path: /{clean_path}")

    for key in config.keys():
        print(f"Config key: {key}")

    if f"/{clean_path}" in config:
        backend_url = config[f"/{clean_path}"]
    else:
        print("Path not found in configuration")
        response = jsonify({'error': 'Path not found'})
        response.status_code = 404
        return add_cors_headers(response)

    if request.method == 'GET':
        response = requests.get(backend_url, params=request.args)
    elif request.method == 'POST':
        headers = {key: value for key, value in request.headers if key != 'Host'}
        response = requests.post(backend_url, json=request.json, headers=headers)
        print(f"Response from backend: {response.status_code}, {response.content}")
    elif request.method == 'OPTIONS':
        return add_cors_headers(Response())

    # Prepare the proxy response
    proxy_response = Response(response.content, response.status_code)

    # Handle the Content-Length explicitly
    proxy_response.headers['Content-Length'] = len(response.content)

    # Add headers to the proxy response
    for header_name, header_value in response.headers.items():
        if header_name.lower() != 'transfer-encoding':  # Skip 'Transfer-Encoding' if present
            proxy_response.headers[header_name] = header_value

    return add_cors_headers(proxy_response)

@app.after_request
def apply_cors_headers(response):
    return add_cors_headers(response)

if __name__ == '__main__':
    load_config()
    config_watcher_thread = threading.Thread(target=watch_config, daemon=True)
    config_watcher_thread.start()
    app.run(host='0.0.0.0', port=93)




