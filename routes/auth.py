from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import jwt
import hashlib

from local_db import get_user, create_user

router = APIRouter()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 60 * 24  # 1 يوم

class User(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register")
def register(user: User):
    existing_user = get_user(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_data = {
        "email": user.email,
        "name": user.name or "",
        "password": hash_password(user.password),
        "created_at": datetime.utcnow().isoformat(),
        "balance": 0,
        "wallet": [],
        "mined": 0,
        "last_mined": None,
    }

    success = create_user(user.email, user_data)
    if not success:
        raise HTTPException(status_code=500, detail="User creation failed")

    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: User):
    db_user = get_user(user.email)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email}, timedelta(minutes=TOKEN_EXPIRATION_MINUTES))
    return {"access_token": token, "token_type": "bearer"}
