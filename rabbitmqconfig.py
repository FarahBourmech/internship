import pika

class RabbitMQConfig:
    def __init__(self, host, port, username, password, ssl_enabled=False):
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=credentials,
            ssl_options=None
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def create_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True)

    def send_message(self, queue_name, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2 
            )
        )
        print(f" [x] Sent {message}")
