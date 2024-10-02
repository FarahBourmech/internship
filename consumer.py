import pika
import json
import requests
import os
from connection.JiraConnection import JiraConnection
from dotenv import load_dotenv
#
load_dotenv()

jira_url_base = os.getenv("url_jira_base")
email = os.getenv("email")
api_token = os.getenv("api_token")

connection = JiraConnection(jira_url_base, email, api_token).connect()

def fetch_jira_ticket(ticket_name):
    url = f"{jira_url_base}{ticket_name}"
    response = requests.get(url, auth=(email, api_token))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch ticket: {response.status_code}")
        return None
#split the description and determine the number of columns
def process_current_description(current_description):
    current_description = current_description.strip() if current_description else ""
    table_element1 = current_description.split("|") if current_description else []
    table_element2 = current_description.split("\n")
    nb_column = len(table_element2)
    return table_element1, nb_column
#determiner l emplacement du type inserer
def find_type_index(table_element1, new_type):
    index_of_type=0
    for i in range (len(table_element1)):
        if table_element1[i]==new_type:
            index_of_type=i
    return index_of_type
    
#determiner le nb de colonne du tableau inseré dans jira table
def count_jira_table_columns(jira_table):
    return jira_table.count('|')

def clean_jira_table(jira_table):
    return [item for item in jira_table.split('|') if item]

def update_table_element(table_element1, index_of_type, jira_table_array):
    for j in range(len(jira_table_array)):
        if index_of_type is not None and index_of_type + 1 + j < len(table_element1):
            table_element1[index_of_type + 1 + j] = jira_table_array[j]

def update_jira_ticket(ticket_name, jira_table, new_type):
    current_data = fetch_jira_ticket(ticket_name)
    if not current_data:
        return
    
    current_description = current_data["fields"].get("description", "")
    table_element1, nb_column = process_current_description(current_description)
    index_of_type = find_type_index(table_element1, new_type)
    num_of_column_jira_table = count_jira_table_columns(jira_table)

    if nb_column != num_of_column_jira_table:
        print("Inconvenience of columns")
        return

    jira_table_array = clean_jira_table(jira_table)
    update_table_element(table_element1, index_of_type, jira_table_array)

    print("Updated table element:", table_element1)

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "description": "|".join(table_element1).strip() 
        }
    }

    update_response = requests.put(
        f"{jira_url_base}{ticket_name}",
        headers=headers,
        data=json.dumps(payload),
        auth=(email, api_token)
    )

    if update_response.status_code == 204:
        print(f"Ticket {ticket_name} updated successfully.")
    else:
        print(f"Failed to update ticket {ticket_name}. Status code: {update_response.status_code}, Response: {update_response.text}")

def start_consumer():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=pika.PlainCredentials('user', 'password')  # Ensure the credentials are correct
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            """Callback function to handle incoming messages."""
            message = json.loads(body.decode())
            print(f" [x] Received {message}")

            ticket_name = message.get("ticketName")
            jira_table = message.get("jiraTable")
            new_type = message.get("type")

            if ticket_name and jira_table:
                update_jira_ticket(ticket_name, jira_table, new_type)
            else:
                print("Invalid message format. Missing 'ticketName' or 'jiraTable'.")

            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='task_queue', on_message_callback=callback)

        channel.start_consuming()
    except Exception as e:
        print(f"Failed to connect to RabbitMQ: {e}")

if __name__ == '__main__':
    start_consumer()
