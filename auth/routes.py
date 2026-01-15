from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserRegister, UserLogin
from database.models import User
from database.session import SessionLocal
from auth.security import (
    hash_password,
    verify_password,
    create_access_token
)
from dependencies import get_db

router = APIRouter(tags=["auth"])

@router.post("/register")
def register(
    data: UserRegister,
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    return {"status": "created"}


@router.post("/login")
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
