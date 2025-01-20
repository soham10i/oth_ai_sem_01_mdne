from fastapi import APIRouter, Depends, HTTPException
from app.services.calendar_service import CalendarService

router = APIRouter()

@router.post("/events")
async def create_event(
    calendar_id: int,
    event_title: str,
    start_datetime: str,
    end_datetime: str,
    is_recurring: bool = False,
    recurrence_rule: str = None,
    recurrence_end_date: str = None,
    access_level: str = "private",
    event_description: str = None,
    service: CalendarService = Depends(CalendarService)
):
    """
    Create a new event in the specified calendar.

    Args:
        calendar_id (int): The ID of the calendar.
        event_title (str): The title of the event.
        start_datetime (str): The start date and time of the event.
        end_datetime (str): The end date and time of the event.
        is_recurring (bool, optional): Whether the event is recurring. Defaults to False.
        recurrence_rule (str, optional): The recurrence rule for the event. Defaults to None.
        recurrence_end_date (str, optional): The end date for the recurrence. Defaults to None.
        access_level (str, optional): The access level of the event. Defaults to "private".
        event_description (str, optional): The description of the event. Defaults to None.
        service (CalendarService, optional): The calendar service dependency.

    Returns:
        dict: A message indicating the event was created successfully and the event ID.
    """
    try:
        event_id = service.create_event(
            calendar_id, event_title, start_datetime, end_datetime,
            is_recurring, recurrence_rule, recurrence_end_date, access_level, event_description
        )
        return {"message": "Event created successfully", "event_id": event_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/events")
async def get_events(calendar_id: int, start_datetime: str = None, end_datetime: str = None, service: CalendarService = Depends(CalendarService)):
    """
    Retrieve events from the specified calendar.

    Args:
        calendar_id (int): The ID of the calendar.
        start_datetime (str, optional): The start date and time to filter events. Defaults to None.
        end_datetime (str, optional): The end date and time to filter events. Defaults to None.
        service (CalendarService, optional): The calendar service dependency.

    Returns:
        dict: A message indicating no events were found or a list of events.
    """
    try:
        events = service.get_events(calendar_id, start_datetime, end_datetime)
        if not events:
            return {"message": "No events found"}
        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/events/{event_id}")
async def delete_event(event_id: int, service: CalendarService = Depends(CalendarService)):
    """
    Delete an event by its ID.

    Args:
        event_id (int): The ID of the event to delete.
        service (CalendarService, optional): The calendar service dependency.

    Returns:
        dict: A message indicating the event was deleted successfully.
    """
    try:
        service.delete_event(event_id)
        return {"message": "Event deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
