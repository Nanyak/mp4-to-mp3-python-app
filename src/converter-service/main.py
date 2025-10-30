
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
from pymongo import MongoClient
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
