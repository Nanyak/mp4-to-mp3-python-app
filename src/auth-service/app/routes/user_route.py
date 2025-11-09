from fastapi import APIRouter, HTTPException
from db import get_connection as get_db_connection
from services.jwt_service import create_access_token, create_refresh_token, verify_refresh_token
from services.hash_service import hash_password
from schemas.user_schema import UserCreate
router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/register")
def register_user(user: UserCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", (user.username, user.email))
    if cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    hashed_password = hash_password(user.password)

    cur.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id, username, email",
        (user.username, user.email, hashed_password)
    )

    new_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_user
