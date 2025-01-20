from fastapi import APIRouter
from app.controllers import mail_controller

router = APIRouter()

router.include_router(mail_controller.router, prefix="", tags=["mail"])
