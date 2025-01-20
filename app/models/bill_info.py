from sqlalchemy import Column, Integer, String, DECIMAL, Date, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from enum import Enum as PyEnum

Base = declarative_base()

class BillInfo(Base):
    __tablename__ = 'Bill_Info'
    
    bill_id = Column(Integer, primary_key=True, autoincrement=True)
    bill_name = Column(String(100), nullable=False)
    bill_type = Column(Enum('gas', 'electricity'), nullable=False)
    total_consumption = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    amount = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    house_id = Column(Integer, ForeignKey('Houses.house_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    access_level = Column(Enum('owner_only', 'shared', 'public'), default='owner_only')
    due_date = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    class BillTypeEnum(PyEnum):
        gas = 'gas'
        electricity = 'electricity'

    class AccessLevelEnum(PyEnum):
        owner_only = 'owner_only'
        shared = 'shared'
        public = 'public'

    class BillInfoResponse(BaseModel):
        bill_id: int
        bill_name: str
        bill_type: str
        total_consumption: Decimal
        amount: Decimal
        house_id: int
        user_id: int
        access_level: str
        due_date: date
        created_at: datetime
        updated_at: datetime

        class Config:
            orm_mode = True