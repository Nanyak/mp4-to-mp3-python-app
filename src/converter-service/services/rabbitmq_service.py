import os
import pika


class RabbitMQService:
    def __init__(self):
        self.host = os.getenv("RABBITMQ_HOST", "localhost")
        self.user = os.getenv("RABBITMQ_USER", "guest")
        self.password = os.getenv("RABBITMQ_PASSWORD", "guest")

        self.connection = None
        self.channel = None

    def get_connection(self):
        """Create and return a new RabbitMQ connection."""
        credentials = pika.PlainCredentials(self.user, self.password)
        params = pika.ConnectionParameters(host=self.host, port=5672, credentials=credentials)
        self.connection = pika.BlockingConnection(params)
        return self.connection

    def get_channel(self):
        """Create and return a new channel."""
        if not self.connection or self.connection.is_closed:
            self.get_connection()
        self.channel = self.connection.channel()
        return self.channel
    def declare_queue(self, queue_name):
        """Declare a durable queue."""
        if not self.channel:
            self.get_channel()
        self.channel.queue_declare(queue=queue_name, durable=True)
    def publish_message(self, queue_name, message):
        """Publish a message to the specified queue."""
        if not self.channel:
            self.get_channel()
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
        )
    def consume_messages(self, queue_name, callback):
        """Consume messages from the specified queue."""
        if not self.channel:
            self.get_channel()
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
    def close(self):
        """Close the connection safely."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
