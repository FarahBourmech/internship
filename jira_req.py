import base64
import json
import os
from connection.JiraConnection import JiraConnection
from dotenv import load_dotenv
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from requests.auth import HTTPBasicAuth

from rabbitmqconfig import RabbitMQConfig

app = Flask(__name__)
CORS(app)

load_dotenv()

jira_url_base = os.getenv("url_jira_base")
email = os.getenv("email")
api_token = os.getenv("api_token")

connection = JiraConnection(jira_url_base,email,api_token).connect()

if not jira_url_base or not email or not api_token:
    raise EnvironmentError("Jira credentials or URL are not set in the environment variables.")


@app.route('/api/v1/greet/<ticket_name>', methods=['GET'])
def greet_user(ticket_name):
    jira_url = f"{jira_url_base}{ticket_name}"
    print(jira_url)
    auth_str = f"{email}:{api_token}"
    print(auth_str)
    auth_bytes = auth_str.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')

    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/json"
    }

    response = requests.get(jira_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        bodies = [comment['body'] for comment in data['fields']['comment']['comments']]

        issue_data = {
            'ProjectKey': data['fields']['project']['key'],
            'ProjectId': data['fields']['project']['id'],
            'ProjectName': data['fields']['project']['name'],
            'issueKey': data['key'],
            'summary': data['fields']['summary'],
            'status': data['fields']['status']['name'],
            'reporter': data['fields']['reporter']['displayName'],
            'assignee': data['fields']['assignee']['displayName'] if data['fields']['assignee'] else None,
            'created': data['fields']['created'],
            'updated': data['fields']['updated'],
            'issueType': data['fields']['issuetype']['name'],
            'issueId': data['fields']['issuetype']['id'],
            'comments': bodies,
            'description': data['fields']['description'],
        }
        print(1)
        send_to_rabbitmq(issue_data)
        print(2)
        return jsonify(issue_data)
    else:
        return jsonify({'error': 'Failed to fetch data from Jira API'}), response.status_code


@app.route('/api/v1/greet/send', methods=['POST'])
def send():
    data = request.json
    ticket_name = data.get('ticketName')
    type = data.get('type')
    description = data.get('jiraTable')

    print(data)

    if not ticket_name or not type or not description:
        return jsonify({'error': 'Ticket name, type, and description are required'}), 400

    send_to_rabbitmq(data)
    return jsonify({'status': 'Message sent to queue'}), 200

def send_to_rabbitmq(data):
    try:
        config = RabbitMQConfig(
            host='localhost',
            port=5672,
            username='user',
            password='password',
            ssl_enabled=False
        )
        config.create_queue('task_queue')

        message = json.dumps(data)
        config.send_message('task_queue', message)
        print(f" [x] Sent message to task_queue: {message}")
    except Exception as e:
        print(f"Failed to send message to RabbitMQ: {e}")



def message_callback(message):
    print(f"Received notification: {message}")
if __name__ == '__main__':
    app.run(debug=True)