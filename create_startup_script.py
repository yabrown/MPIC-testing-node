import requests
import base64
import json
import os

# Replace with your actual Vultr API key
API_KEY = os.environ.get('VULTR_API_KEY')

# Path to your startup script file
script_file_path = 'vultr-startup-script.sh'

# Read the script file
with open(script_file_path, 'r') as file:
    script_content = file.read()

# Base64 encode the script content
encoded_script = base64.b64encode(script_content.encode('utf-8')).decode('utf-8')

# API endpoint for creating a startup script
url = 'https://api.vultr.com/v2/startup-scripts'

# Headers for the API request
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Data payload for the API request
data = {
    'name': 'test node',  # Replace with your desired script name
    'script': encoded_script,
    'type': 'boot'  # 'boot' for boot scripts; use 'pxe' for PXE scripts
}

# Send the POST request to create the startup script
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 201:
    # Parse the JSON response
    response_data = response.json()
    # Retrieve the script ID
    script_id = response_data['startup_script']['id']
    print(f'Startup script created successfully with ID: {script_id}')
else:
    print(f'Failed to create startup script. Status code: {response.status_code}')
    print(f'Response: {response.text}')
