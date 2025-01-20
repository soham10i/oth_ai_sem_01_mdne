from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, TIMESTAMP, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class CalendarEvent(Base):
    __tablename__ = 'Calendar_Event'
    
    calendar_event_id = Column(Integer, primary_key=True, autoincrement=True)
    calendar_id = Column(Integer, ForeignKey('Calendar.calendar_id'), nullable=False)
    event_title = Column(String(255), nullable=False)
    event_description = Column(Text)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    access_level = Column(Enum('private', 'shared', 'public'), default='private')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
