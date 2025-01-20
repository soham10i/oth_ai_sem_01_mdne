from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()

class House(Base):
    __tablename__ = 'houses'
    
    house_id = Column(Integer, primary_key=True, autoincrement=True)
    house_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class HouseBase(BaseModel):
    house_name: str
    address: str
    owner_id: int

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class HouseCreate(HouseBase):
    pass

class HouseResponse(HouseBase):
    house_id: int
    created_at: datetime
    updated_at: datetime
