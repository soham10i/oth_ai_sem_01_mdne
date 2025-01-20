from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()

class Resident(Base):
    __tablename__ = 'Residents'
    
    resident_id = Column(Integer, primary_key=True, autoincrement=True)
    house_id = Column(Integer, ForeignKey('Houses.house_id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class ResidentBase(BaseModel):
    house_id: int
    user_id: int

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class ResidentCreate(ResidentBase):
    pass

class ResidentResponse(ResidentBase):
    resident_id: int
    created_at: datetime
    updated_at: datetime
