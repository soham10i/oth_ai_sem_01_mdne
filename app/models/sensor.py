from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
"""
This module defines the SQLAlchemy model and Pydantic schemas for the Sensor entity.
Classes:
    Sensor(Base): SQLAlchemy model for the 'Sensors_Info' table.
        Attributes:
            sensor_id (int): Primary key, auto-incremented.
            sensor_name (str): Name of the sensor.
            sensor_type (str): Type of the sensor.
            sensor_manufacturer (str): Manufacturer of the sensor.
            house_id (int): Foreign key referencing the 'Houses' table.
            sensor_unit (str): Unit of measurement for the sensor.
            created_at (datetime): Timestamp when the sensor record was created.
            updated_at (datetime): Timestamp when the sensor record was last updated.
    SensorBase(BaseModel): Pydantic base schema for Sensor.
        Attributes:
            sensor_name (str): Name of the sensor.
            sensor_type (str): Type of the sensor.
            sensor_manufacturer (str): Manufacturer of the sensor.
            house_id (int): Foreign key referencing the 'Houses' table.
            sensor_unit (str): Unit of measurement for the sensor.
    SensorCreate(SensorBase): Pydantic schema for creating a new Sensor.
        Inherits all attributes from SensorBase.
    SensorResponse(SensorBase): Pydantic schema for returning a Sensor response.
        Attributes:
            sensor_id (int): Primary key, auto-incremented.
            created_at (datetime): Timestamp when the sensor record was created.
            updated_at (datetime): Timestamp when the sensor record was last updated.
"""
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
