from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()

class Sensor(Base):
    __tablename__ = 'Sensors_Info'
    
    sensor_id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_name = Column(String(100), nullable=False)
    sensor_type = Column(String(50), nullable=False)
    sensor_manufacturer = Column(String(100), nullable=False)
    house_id = Column(Integer, ForeignKey('Houses.house_id'), nullable=False)
    sensor_unit = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class SensorBase(BaseModel):
    sensor_name: str
    sensor_type: str
    sensor_manufacturer: str
    house_id: int
    sensor_unit: str

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class SensorCreate(SensorBase):
    pass

class SensorResponse(SensorBase):
    sensor_id: int
    created_at: datetime
    updated_at: datetime
