import psycopg2
import psycopg2.extras
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
security = HTTPBasic()
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DATABASE_HOST'),
        database=os.getenv('DATABASE_NAME'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        port=os.getenv('DATABASE_PORT'))
    return conn
@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    auth_table_name = os.getenv('AUTH_TABLE_NAME')
    username = credentials.username
    password = credentials.password
    if not username or not password:
        raise HTTPException(status_code=401, detail="Missing username or password")
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = f"SELECT username, password FROM {auth_table_name} WHERE username = %s"
    cur.execute(query, (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if password != user["password"]:
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"message": f"Welcome {username}!"}