
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os, time
from pymongo import MongoClient
import gridfs, pika
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
security = HTTPBasic()

def get_database():
    client = MongoClient(
        host=os.getenv("MONGO_HOST"),
        port=int(os.getenv("MONGO_PORT")),
        username=os.getenv("MONGO_USER"),
        password=os.getenv("MONGO_PASSWORD"),
        authSource="admin"    
    )
    db = client[os.getenv("MONGO_DB_NAME")]
    return db
db = get_database()
fs_videos = gridfs.GridFS(db, collection="videos")
fs_audios = gridfs.GridFS(db, collection="audios")


# RabbitMQ connection (per request)
def get_rabbit_connection():
    credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASSWORD"))
    params = pika.ConnectionParameters("rabbit-mq", port=5672, credentials=credentials)
    return pika.BlockingConnection(params)

@app.get("/test_queue")
def test_queue():
    connection = get_rabbit_connection()
    channel = connection.channel()
    channel.queue_declare(queue='converter', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='converter',
        body='Converter Service is up and running!',
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()
    return {"status": "message sent"}
@app.get("/insert_customer")
def insert_customer():
    customers = db["customers"]
    mydict = {"name": "John", "address": "Highway 37"}
    result = customers.insert_one(mydict)
    return {"inserted_id": str(result.inserted_id)}
@app.delete("/delete_customers")
def delete_customers():
    customers = db["customers"]
    result = customers.delete_many({})
    return {"deleted_count": result.deleted_count}
