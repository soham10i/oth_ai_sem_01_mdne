from fastapi import APIRouter
from app.controllers import sensor_controller

router = APIRouter()

router.include_router(sensor_controller.router, prefix="", tags=["sensor"])
