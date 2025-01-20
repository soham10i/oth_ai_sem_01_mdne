from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models.sensor_data import SensorDataModel
from app.services.mongo_service import fetch_sensor_data_by_house_id, fetch_sensor_data_by_sensor_id, \
        fetch_and_store_sensor_data_in_mongo, store_all_influxdb_data_in_mongo
from app.services.sensor_data_service import generate_sensor_data_for_house, dump_sensor_data_to_influxdb
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter()

def check_admin_user(current_user: User):
    if current_user.user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")

@router.get("/house/{house_id}", response_model=List[SensorDataModel])
def get_sensor_data_by_house_id(house_id: int, current_user: User = Depends(get_current_user)):
    check_admin_user(current_user)
    try:
        sensor_data = fetch_sensor_data_by_house_id(house_id)
        if not sensor_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No sensor data found for the given house ID")
        return sensor_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/sensor/{sensor_id}", response_model=SensorDataModel)
def get_sensor_data_by_sensor_id(sensor_id: int, current_user: User = Depends(get_current_user)):
    check_admin_user(current_user)
    try:
        sensor_data = fetch_sensor_data_by_sensor_id(sensor_id)
        if not sensor_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No sensor data found for the given sensor ID")
        return sensor_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/generate/{house_id}", response_model=SensorDataModel)
def generate_sensor_data(house_id: int, current_user: User = Depends(get_current_user)):
    check_admin_user(current_user)
    try:
        sensor_data = generate_sensor_data_for_house(house_id)
        return sensor_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/dump/{house_id}", response_model=SensorDataModel)
def dump_sensor_data(house_id: int, current_user: User = Depends(get_current_user)):
    check_admin_user(current_user)
    try:
        sensor_data = generate_sensor_data_for_house(house_id)
        dump_sensor_data_to_influxdb(sensor_data)
        return sensor_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/dump_to_mongo/{house_id}", response_model=SensorDataModel)
def dump_sensor_data_to_mongo(house_id: int, current_user: User = Depends(get_current_user)):
    check_admin_user(current_user)
    try:
        fetch_and_store_sensor_data_in_mongo(house_id)
        sensor_data = fetch_sensor_data_by_house_id(house_id)
        if not sensor_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No sensor data found for the given house ID")
        return sensor_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/dump_all_influxdb_to_mongo")
def dump_all_influxdb_to_mongo(current_user: User = Depends(get_current_user)):
    check_admin_user(current_user)
    try:
        store_all_influxdb_data_in_mongo()
        return {"message": "All InfluxDB data dumped to MongoDB successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

