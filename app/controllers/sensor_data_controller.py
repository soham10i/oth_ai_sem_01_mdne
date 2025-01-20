from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models.sensor_data import SensorDataModel
from app.services.mongo_service import fetch_sensor_data_by_house_id, fetch_sensor_data_by_sensor_id, \
        fetch_and_store_sensor_data_in_mongo, store_all_influxdb_data_in_mongo
from app.services.sensor_data_service import fetch_all_house_ids, generate_sensor_data_for_house, dump_sensor_data_to_influxdb, periodic_generate_sensor_data_for_house
from app.services.auth_service import get_current_user
from app.models.user import User
import schedule
import threading
import time
from app.database.mongo_connection import connect

router = APIRouter()

scheduler_thread = None
scheduler_running = False

def start_scheduler():
    global scheduler_thread, scheduler_running
    if not scheduler_running:
        scheduler_running = True
        schedule.every(10).seconds.do(generate_sensor_data_periodically)
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.start()

def stop_scheduler():
    global scheduler_running
    scheduler_running = False

def run_scheduler():
    while scheduler_running:
        schedule.run_pending()
        time.sleep(1)

def generate_sensor_data_periodically():
    house_ids = fetch_all_house_ids()
    for house_id in house_ids:
        periodic_generate_sensor_data_for_house(house_id)

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

@router.post("/scheduler/start")
async def scheduler_start(current_user: User = Depends(get_current_user)):
    check_admin_user(current_user)
    try:
        start_scheduler()
        return {"message": "Scheduler started successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/scheduler/stop")
async def scheduler_stop(current_user: User = Depends(get_current_user)):
    check_admin_user(current_user)
    try:
        stop_scheduler()
        return {"message": "Scheduler stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/mongo/house/{house_id}", response_model=List[SensorDataModel])
def get_mongo_sensor_data_by_house_id(house_id: int, current_user: User = Depends(get_current_user)):
    check_admin_user(current_user)
    try:
        db = connect()
        sensor_data = list(db.sensor_data.find({"house_id": house_id}))
        if not sensor_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No sensor data found in MongoDB for the given house ID")
        return sensor_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

