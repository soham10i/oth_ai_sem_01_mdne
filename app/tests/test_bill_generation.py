import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_bills_schedule():
    response = client.get("/bills/schedule")
    assert response.status_code == 200
    assert response.json() == {
        "schedule": [
            {"day": "Monday", "time": "09:00"},
            {"day": "Wednesday", "time": "09:00"},
            {"day": "Friday", "time": "09:00"}
        ]
    }