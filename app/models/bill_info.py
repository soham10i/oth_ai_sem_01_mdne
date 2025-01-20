from sqlalchemy import Column, Integer, String, DECIMAL, Date, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

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
