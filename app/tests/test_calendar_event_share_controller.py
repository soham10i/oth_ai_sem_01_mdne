import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_share_event():
    response = client.post("/events/share", json={
        "event_id": 1,
        "shared_with_user_id": 2,
        "share_access_level": "view"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Event shared successfully"

def test_get_shared_events():
    response = client.get("/events/shared", params={"user_id": 2})
    assert response.status_code == 200
    assert "shared_events" in response.json()

def test_update_share_access():
    response = client.put("/events/share/1", json={"share_access_level": "edit"})
    assert response.status_code == 200
    assert response.json()["message"] == "Share access level updated successfully"
