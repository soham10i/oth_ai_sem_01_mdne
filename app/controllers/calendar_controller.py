from fastapi import FastAPI, APIRouter, Depends, HTTPException
from app.services.calendar_service import CalendarService

router = APIRouter()

@router.post("/calendars")
async def create_calendar(user_id: int, calendar_name: str, description: str = None, service: CalendarService = Depends(CalendarService)):
    calendar_id = service.create_calendar(user_id, calendar_name, description)
    return {"message": "Calendar created successfully", "calendar_id": calendar_id}

@router.get("/calendars")
async def get_calendars(user_id: int, service: CalendarService = Depends(CalendarService)):
    calendars = service.get_calendars(user_id)
    if not calendars:
        return {"message": "No calendars found"}
    return {"calendars": calendars}

@router.delete("/calendars/{calendar_id}")
async def delete_calendar(calendar_id: int, service: CalendarService = Depends(CalendarService)):
    service.delete_calendar(calendar_id)
    return {"message": "Calendar deleted successfully"}


