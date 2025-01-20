from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.user import UserCreate
from app.services.auth_service import create_user, get_current_user, get_user_by_email, authenticate_user, create_access_token, create_refresh_token
from app.database.connection import get_db

class LoginRequest(BaseModel):
    email: str
    password: str

class UserController:
    router = APIRouter()

    @router.post("/register", response_model=UserCreate)
    def register_user(user: UserCreate, db: Session = Depends(get_db)):
        try:
            db_user = get_user_by_email(db, email=user.email)
            if db_user:
                raise HTTPException(
                    status_code=400, detail="Email already registered")
            return create_user(db, user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/login")
    def login_user(login_request: LoginRequest, db: Session = Depends(get_db)):
        try:
            user = authenticate_user(
                db, login_request.email, login_request.password)
            if not user:
                raise HTTPException(
                    status_code=400, detail="Invalid email or password")

            access_token = create_access_token(data={"sub": user.email})
            refresh_token = create_refresh_token(data={"sub": user.email})

            return {
                "email": user.email,
                "username": user.username,
                "user_type": user.user_type,
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
