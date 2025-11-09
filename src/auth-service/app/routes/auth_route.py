import psycopg2
import psycopg2.extras
from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from schemas.auth_schema import LoginRequest, TokenResponse
from dotenv import load_dotenv
from db import get_connection as get_db_connection
from services.jwt_service import create_access_token, create_refresh_token, verify_refresh_token
from services.hash_service import verify_password
load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["Auth"])
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (request.username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = user["id"]
    access_token = create_access_token({"sub": str(user_id)})
    refresh_token = create_refresh_token({"sub": str(user_id)})

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET refresh_token=%s WHERE id=%s", (refresh_token, user_id))
    conn.commit()
    cur.close()
    conn.close()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str):
    payload = verify_refresh_token(refresh_token)
    user_id = payload.get("sub")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT refresh_token FROM users WHERE id = %s", (user_id,))
    stored_token = cur.fetchone()
    cur.close()
    conn.close()

    if not stored_token or stored_token["refresh_token"] != refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return TokenResponse(
        access_token=create_access_token({"sub": user_id}),
        refresh_token=refresh_token
    )
