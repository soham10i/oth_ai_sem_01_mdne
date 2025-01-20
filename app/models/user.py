from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    dob = Column(Date)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    user_type = Column(String(50), nullable=False, default='resident')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    dob: datetime
    email: EmailStr

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d')
        }

class UserCreate(UserBase):
    password: str
    user_type: str

    @field_validator('user_type')
    def user_type_lowercase(cls, v):
        if v.lower() not in ['resident', 'owner', 'admin']:
            raise ValueError('Invalid user type')
        return v.lower()

class UserResponse(UserBase):
    user_id: int
    user_type: str

    @field_validator('user_type')
    def user_type_lowercase(cls, v):
        if v.lower() not in ['resident', 'owner', 'admin']:
            raise ValueError('Invalid user type')
        return v.lower()
