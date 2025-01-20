from sqlalchemy import Column, Integer, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Notification(Base):
    __tablename__ = 'Notification'
    
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    calendar_event_id = Column(Integer, ForeignKey('Calendar_Event.calendar_event_id'), nullable=True)
    bill_id = Column(Integer, ForeignKey('Bill_Info.bill_id'), nullable=True)
    notification_type = Column(Enum('calendar_event', 'bill_info'), nullable=False)
    read_status = Column(Enum('unread', 'read'), default='unread')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
