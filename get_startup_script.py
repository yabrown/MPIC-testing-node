import requests
import base64
import os

# Replace with your actual Vultr API key and the ID of the script you want to retrieve
API_KEY = os.environ.get('VULTR_API_KEY')
SCRIPT_ID_ARI = os.environ.get('STARTUP_SCRIPT_ID')
SCRIPT_ID_CHR = os.environ.get('STARTUP_CHR')

# API endpoint for retrieving an existing startup script
url = f'https://api.vultr.com/v2/startup-scripts/{SCRIPT_ID_CHR}'

# Headers for the API request
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Send the GET request to retrieve the startup script
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    response_data = response.json()
    # Get the encoded script content
    encoded_script = response_data['startup_script']['script']
    # Decode the script content from base64
    script_content = base64.b64decode(encoded_script).decode('utf-8')
    # Display the script content
    print(f"Script Name: {response_data['startup_script']['name']}")
    print("Script Content:")
    print(script_content)
else:
    print(f'Failed to retrieve startup script. Status code: {response.status_code}')
    print(f'Response: {response.text}')
