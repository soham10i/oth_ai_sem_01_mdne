from fastapi import APIRouter, HTTPException, status, Depends
from app.models.sensor import SensorCreate, SensorResponse
from app.services.sensor_service import add_sensor, update_sensor, delete_sensor, get_sensor, get_sensors_by_house
from app.database.connection import get_db
from sqlalchemy.orm import Session
from app.services.auth_service import get_current_user
from app.models.user import User
from typing import List

router = APIRouter()

def check_user_type(current_user: User):
    if current_user.user_type not in ['owner', 'admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

@router.post("/add", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
def add_sensor_data(sensor: SensorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_user_type(current_user)
    db_sensor = add_sensor(sensor)
    if not db_sensor:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sensor could not be added")
    return db_sensor

# Sample request body for /add endpoint
"""
{
    "sensor_name": "Temperature Sensor",
    "sensor_type": "temperature",
    "sensor_manufacturer": "SensorTech",
    "house_id": 1,
    "sensor_unit": "C"
}
"""

@router.put("/update/{sensor_id}", response_model=SensorResponse)
def update_sensor_data(sensor_id: int, sensor: SensorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_user_type(current_user)
    db_sensor = update_sensor(sensor_id, sensor)
    if not db_sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    return db_sensor

@router.delete("/delete/{sensor_id}", response_model=SensorResponse)
def delete_sensor_data(sensor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_user_type(current_user)
    db_sensor = delete_sensor(sensor_id)
    if not db_sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    return db_sensor

@router.get("/fetch/{sensor_id}", response_model=SensorResponse)
def fetch_sensor_data(sensor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_user_type(current_user)
    db_sensor = get_sensor(sensor_id)
    if not db_sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    return db_sensor

@router.get("/fetch/house/{house_id}", response_model=List[SensorResponse])
def fetch_sensors_by_house(house_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_user_type(current_user)
    sensors = get_sensors_by_house(house_id)
    return sensors
