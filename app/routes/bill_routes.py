from fastapi import APIRouter
from app.controllers import bill_controller

router = APIRouter()

router.include_router(bill_controller.router, prefix="", tags=["houses"])

