from sqlalchemy.orm import Session
from app.auth.security import get_password_hash, verify_password
from app.auth.repository import UserRepository
from fastapi import HTTPException

class AuthService:
    @staticmethod
    def create_user(db: Session, *, email: str, username: str, password: str) -> str:
        if UserRepository.get_by_email(db, email):
          raise HTTPException(status_code=400,detail="Email already exists")
        
        if UserRepository.get_by_username(db, username):
          raise HTTPException( status_code=400, detail="Username already exists")
        
      
        hashed_password = get_password_hash(password)
        return UserRepository.create(
            db, email=email, username=username, hashed_password=hashed_password
        )

    @staticmethod
    def authenticate(db: Session, email: str, password: str):
        user = UserRepository.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None

        return user
