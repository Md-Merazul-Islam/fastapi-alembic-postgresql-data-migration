from sqlalchemy.orm import Session
from app.auth.schema import UserCreate, UserOut,  Token
from app.core.database import SessionLocal
from app.auth.security import create_access_token
from fastapi import APIRouter, Depends, HTTPException
from app.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return AuthService.create_user(
        db, email=user.email, username=user.username, password=user.password
    )

from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str
    
@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = AuthService.authenticate(db, request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}