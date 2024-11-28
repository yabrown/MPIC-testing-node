import requests
import base64
import json
import os

# Replace with your actual Vultr API key and the ID of the script you want to update
API_KEY = os.environ.get('VULTR_API_KEY')
SCRIPT_ID_ARI = os.environ.get('STARTUP_SCRIPT_ID')
SCRIPT_ID_CHR = os.environ.get('STARTUP_CHR')

# Path to your new script file
new_script_file_path = 'vultr-startup-script.sh'

# Read the new script file
with open(new_script_file_path, 'r') as file:
    new_script_content = file.read()

# Base64 encode the new script content
encoded_script = base64.b64encode(new_script_content.encode('utf-8')).decode('utf-8')

# API endpoint for updating an existing startup script
url = f'https://api.vultr.com/v2/startup-scripts/{SCRIPT_ID_ARI}'

# Headers for the API request
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Data payload for the API request
data = {
    'name': 'test node',  # Update the script name if desired
    'script': encoded_script
}

# Send the PATCH request to update the startup script
response = requests.patch(url, headers=headers, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 204:
    print(f'Startup script with ID {SCRIPT_ID_ARI} updated successfully.')
else:
    print(f'Failed to update startup script. Status code: {response.status_code}')
    print(f'Response: {response.text}')
