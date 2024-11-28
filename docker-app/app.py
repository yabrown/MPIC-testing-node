import collections
import json
from flask import Flask, request, jsonify
from datetime import datetime, timezone
import requests
from loggers import http_logger, error_logger, general_logger, access_logger

app = Flask(__name__)

# Path to your JSON file-- token-indexed IP address history (Google and Open MPIC) will be stored here
STORAGE_FILE = 'vantage_point_info.json'


# Load existing data from the JSON file into tokenMap on app start/restart
try:
    with open(STORAGE_FILE, 'r') as file:
        tokenMap = collections.defaultdict(list, json.load(file))
except (FileNotFoundError, json.JSONDecodeError):
    # Initialize an empty defaultdict if the file does not exist or is invalid
    tokenMap = collections.defaultdict(list)

def save_to_storage():
    """Save the current state of tokenMap to the JSON file."""
    with open(STORAGE_FILE, 'w') as file:
        json.dump(tokenMap, file, indent=4)

@app.before_request
def log_request_info():
    # Log each incoming request
    access_logger.info(f"Request: {request.method} {request.path}")

@app.after_request
def log_response_info(response):
    # Log each outgoing response with a readable format
    http_logger.info(f"Response: {response.status} - {response.headers} - {response.get_data(as_text=True)}")
    return response

@app.route("/info", methods=['GET'])
def handle_info():
    return jsonify({  
        'message': 'Node container is up and running!',
        'num_tokens': len(tokenMap),
        'tokens': list(tokenMap.keys())
    }), 200

    
@app.route('/.well-known/<path:middle>/<token>', methods=['GET'])
def handle_well_known(middle, token):
    timestamp = datetime.now(timezone.utc).isoformat()
    # Extract token, datacenter, origin IP address
    datacenter = request.args.get('datacenter')
    ip_address = request.remote_addr
    if not token:
        return jsonify({'error': 'Token parameter is required'}), 400
    
    general_logger.info(f"Received well-known request with  IP address {ip_address}, token='{token}', middle={middle}, datacenter='{datacenter}'")
    # Create an entry with the required structure
    entry = {
        "ip_address": ip_address,
        "datacenter": datacenter,
        "token": token,
        "timestamp": timestamp

    }

    # Store this request, return error if can't
    try:
        tokenMap[token].append(entry)
        save_to_storage()  # Save changes to file
    except Exception as e:
        error_logger("Error storing VP request in tokenMap: ", e)
        return jsonify("Error storing VP request: ", e), 400

    # if acme (like cerbot) forward this request to the main machine (running certbot) to validate
    if middle == 'acme-challenge':
        general_logger.info("Middle of path is 'acme-challenge', handling potential certbot request by redirecting for success") 
        # the server that certbot is running on (where it stored the nonce). should be the control server.
        # Really need a better way of automating this-- should update with new control server.
        certbot_server_ip = "45.77.138.147"
        certbot_request = f"http://{certbot_server_ip}/.well-known/{middle}/{token}"
        http_logger.info("Redirecting request to cerbot server: ", certbot_request)
        try:
            response = requests.get(certbot_request)
            response.raise_for_status()
            http_logger.info("Redirecting response from certbot server: ", response)
            # This response is specifically configured for certbot (plaintext response)-- won't accept json
            return response.content, 200, {'Content-Type': 'text/plain'}
        except Exception as e:
        # Log the error and return an appropriate error response
            error_logger.info("Error redirecting request to certbot: ", e)
            return f"Error redirecting request: {e}", 500

    # Optionally, return a response
    return jsonify({'message': f'Token {token}, IP, and data center logged successfully'}), 200


@app.route('/getips', methods=['GET'])
def get_ips():
    token = request.args.get('token')
    general_logger.info(f"Executing /getips with token {token}")
    if not token:
        general_logger.info("Token parameter was falsey, returning error")
        return jsonify({'error': 'Token parameter is required'}), 400

    if request.args.get('verbose') == 'true':
        general_logger.info("Searching for token")
        general_logger.info(f"Token {'DOES' if tokenMap[token] else 'DOES NOT'} exist in tokenMap.")
        general_logger.info("Returning verbose IP addresses")
        return jsonify({'verbose_ip_addresses': tokenMap[token]}), 200
    else:
        general_logger.info("Searching for token")
        general_logger.info(f"Token {'DOES' if tokenMap[token] else 'DOES NOT'} exist in tokenMap.")
        ip_list = [entry["ip_address"] for entry in tokenMap[token]]
        general_logger.info(f"Returning IP addresses: {ip_list}")
        return jsonify({'ip_addresses': ip_list}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
