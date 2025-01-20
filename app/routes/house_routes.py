from fastapi import APIRouter
from app.controllers import house_controller

router = APIRouter()

router.include_router(house_controller.router, prefix="", tags=["houses"])

