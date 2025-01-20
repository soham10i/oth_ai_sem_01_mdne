import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_calendar():
    response = client.post("/calendars", json={"user_id": 1, "calendar_name": "Work", "description": "Work calendar"})
    assert response.status_code == 200
    assert response.json()["message"] == "Calendar created successfully"

def test_get_calendars():
    response = client.get("/calendars", params={"user_id": 1})
    assert response.status_code == 200
    assert "calendars" in response.json()

def test_delete_calendar():
    response = client.delete("/calendars/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Calendar deleted successfully"
