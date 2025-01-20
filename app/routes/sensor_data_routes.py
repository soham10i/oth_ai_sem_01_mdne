from fastapi import APIRouter
from app.controllers.sensor_data_controller import router as sensor_data_router

router = APIRouter()
router.include_router(sensor_data_router, prefix="", tags=["Sensor Data"])
