from fastapi import APIRouter, Depends, HTTPException
from app.services.calendar_service import CalendarService

router = APIRouter()

@router.post("/events/share")
async def share_event(event_id: int, shared_with_user_id: int, share_access_level: str = "view", service: CalendarService = Depends(CalendarService)):
    """
    Share an event with another user.

    Args:
        event_id (int): The ID of the event to share.
        shared_with_user_id (int): The ID of the user to share the event with.
        share_access_level (str, optional): The access level for the shared event. Defaults to "view".
        service (CalendarService, optional): The calendar service dependency.

    Returns:
        dict: A message indicating the event was shared successfully.
    """
    try:
        service.share_event(event_id, shared_with_user_id, share_access_level)
        return {"message": "Event shared successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/events/shared")
async def get_shared_events(user_id: int, service: CalendarService = Depends(CalendarService)):
    """
    Retrieve events shared with the specified user.

    Args:
        user_id (int): The ID of the user.
        service (CalendarService, optional): The calendar service dependency.

    Returns:
        dict: A message indicating no shared events were found or a list of shared events.
    """
    try:
        events = service.get_shared_events(user_id)
        if not events:
            return {"message": "No shared events found"}
        return {"shared_events": events}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/events/share/{event_share_id}")
async def update_share_access(event_share_id: int, share_access_level: str, service: CalendarService = Depends(CalendarService)):
    """
    Update the access level for a shared event.

    Args:
        event_share_id (int): The ID of the shared event.
        share_access_level (str): The new access level for the shared event.
        service (CalendarService, optional): The calendar service dependency.

    Returns:
        dict: A message indicating the share access level was updated successfully.
    """
    try:
        service.update_share_access(event_share_id, share_access_level)
        return {"message": "Share access level updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
