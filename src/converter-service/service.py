import os
import gridfs, pika
from dotenv import load_dotenv

load_dotenv()


credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASSWORD"))
params = pika.ConnectionParameters("rabbit-mq", port=5672, credentials=credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='converter', durable=True)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # Here would be the logic to process the conversion task

channel.basic_consume(queue='converter', on_message_callback=callback, auto_ack=True)

channel.start_consuming()