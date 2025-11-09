import psycopg2
import psycopg2.extras
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
from schemas.auth_schema import LoginRequest
from dotenv import load_dotenv
from db import init_db
from routes import user_route, auth_route
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_route.router)
app.include_router(auth_route.router)