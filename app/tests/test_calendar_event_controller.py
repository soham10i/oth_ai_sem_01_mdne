import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_event():
    response = client.post("/events", json={
        "calendar_id": 1,
        "event_title": "Meeting",
        "start_datetime": "2023-10-10T09:00:00",
        "end_datetime": "2023-10-10T10:00:00",
        "is_recurring": False,
        "access_level": "private",
        "event_description": "Team meeting"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Event created successfully"

def test_get_events():
    response = client.get("/events", params={"calendar_id": 1})
    assert response.status_code == 200
    assert "events" in response.json()

def test_delete_event():
    response = client.delete("/events/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Event deleted successfully"
