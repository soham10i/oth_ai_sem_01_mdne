from fastapi import APIRouter
from app.controllers import residents_controller

router = APIRouter()

router.include_router(residents_controller.router, prefix="", tags=["residents"])
