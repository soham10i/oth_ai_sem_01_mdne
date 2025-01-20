from fastapi import APIRouter
from app.controllers.auth_controller import UserController

router = APIRouter()

router.include_router(UserController.router, prefix="", tags=["auth"])
