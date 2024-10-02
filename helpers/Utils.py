# jira_utils.py
import base64
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

jira_url_base = os.getenv("url_jira_base")
email = os.getenv("email")
api_token = os.getenv("api_token")

def update_jira_issue(ticket_name, description):
    """Update the Jira issue with the provided description."""
    jira_url = f"{jira_url_base}{ticket_name}"

    auth_str = f"{email}:{api_token}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(auth_str.encode('ascii')).decode('ascii')}",
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "description": description
        }
    }

    # Send a PUT request to update Jira issue
    response = requests.put(jira_url, headers=headers, json=payload)

    if response.status_code == 204:  # Success status for updates
        print(f"Jira issue {ticket_name} updated successfully.")
    else:
        print(f"Failed to update Jira issue {ticket_name}. Status code: {response.status_code}")
