"""
This module provides API endpoints for managing sensors in a smart home management system.

Endpoints:
    - POST /add: Add a new sensor.
    - PUT /update/{sensor_id}: Update an existing sensor.
    - DELETE /delete/{sensor_id}: Delete a sensor.
    - GET /fetch/{sensor_id}: Fetch a sensor by its ID.
    - GET /fetch/house/{house_id}: Fetch all sensors for a specific house.

Functions:
    check_user_type(current_user: User): Checks if the current user has the required permissions.
    add_sensor_data(sensor: SensorCreate, db: Session, current_user: User): Adds a new sensor.
    update_sensor_data(sensor_id: int, sensor: SensorCreate, db: Session, current_user: User): Updates an existing sensor.
    delete_sensor_data(sensor_id: int, db: Session, current_user: User): Deletes a sensor.
    fetch_sensor_data(sensor_id: int, db: Session, current_user: User): Fetches a sensor by its ID.
    fetch_sensors_by_house(house_id: int, db: Session, current_user: User): Fetches all sensors for a specific house.
"""

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
    try:
        check_user_type(current_user)
        db_sensor = add_sensor(sensor)
        if not db_sensor:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sensor could not be added")
        return db_sensor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update/{sensor_id}", response_model=SensorResponse)
def update_sensor_data(sensor_id: int, sensor: SensorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        check_user_type(current_user)
        db_sensor = update_sensor(sensor_id, sensor)
        if not db_sensor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
        return db_sensor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{sensor_id}", response_model=SensorResponse)
def delete_sensor_data(sensor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        check_user_type(current_user)
        db_sensor = delete_sensor(sensor_id)
        if not db_sensor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
        return db_sensor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fetch/{sensor_id}", response_model=SensorResponse)
def fetch_sensor_data(sensor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        check_user_type(current_user)
        db_sensor = get_sensor(sensor_id)
        if not db_sensor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
        return db_sensor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fetch/house/{house_id}", response_model=List[SensorResponse])
def fetch_sensors_by_house(house_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        check_user_type(current_user)
        sensors = get_sensors_by_house(house_id)
        return sensors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
