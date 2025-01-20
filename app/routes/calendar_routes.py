from fastapi import APIRouter
from app.controllers import calendar_controller, calendar_event_controller, calendar_event_share_controller

router = APIRouter()

router.include_router(calendar_controller.router, prefix="", tags=["calendars"])


