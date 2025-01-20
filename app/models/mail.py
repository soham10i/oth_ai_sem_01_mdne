from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()

class UserMail(Base):
    __tablename__ = 'User_Mail'
    
    user_mail_id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'), nullable=False)
    mail_access_level = Column(Enum('private', 'public', 'restricted'), default='private')
    subject = Column(String(255), nullable=False)
    message = Column(Text)
    mail_status = Column(Enum('unread', 'read'), default='unread')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class UserMailBase(BaseModel):
    sender_id: int
    receiver_id: int
    mail_access_level: str
    subject: str
    message: str
    mail_status: str

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class UserMailCreate(UserMailBase):
    pass

class UserMailResponse(UserMailBase):
    user_mail_id: int
    created_at: datetime
    updated_at: datetime
