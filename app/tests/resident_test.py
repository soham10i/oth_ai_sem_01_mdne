import pytest
from fastapi.testclient import TestClient
from app.controllers.residents_controller import router
from unittest.mock import patch, MagicMock

client = TestClient(router)

@patch('app.services.resident_service.create_resident')
def test_add_resident(mock_create_resident):
    mock_create_resident.return_value = MagicMock()
    resident_data = {
        "name": "Test Resident",
        "email": "test@example.com",
        "house_id": 1
    }
    response = client.post("/add", json=resident_data)
    assert response.status_code == 201
    mock_create_resident.assert_called_once()

@patch('app.services.resident_service.get_residents')
def test_fetch_all_residents(mock_get_residents):
    mock_get_residents.return_value = [MagicMock()]
    response = client.get("/fetchAll")
    assert response.status_code == 200
    mock_get_residents.assert_called_once()

@patch('app.services.resident_service.get_residents_by_house')
def test_fetch_residents_by_house(mock_get_residents_by_house):
    mock_get_residents_by_house.return_value = [MagicMock()]
    response = client.get("/fetch/house", params={"house_id": 1})
    assert response.status_code == 200
    mock_get_residents_by_house.assert_called_once_with(1)

@patch('app.services.resident_service.update_resident')
def test_update_resident_details(mock_update_resident):
    mock_update_resident.return_value = MagicMock()
    resident_data = {
        "name": "Updated Resident",
        "email": "updated@example.com",
        "house_id": 1
    }
    response = client.put("/update", json=resident_data)
    assert response.status_code == 200
    mock_update_resident.assert_called_once()

@patch('app.services.resident_service.delete_resident')
def test_delete_resident_details(mock_delete_resident):
    mock_delete_resident.return_value = MagicMock()
    response = client.delete("/delete", params={"resident_id": 1})
    assert response.status_code == 200
    mock_delete_resident.assert_called_once_with(1)

@patch('app.services.resident_service.get_resident_by_id')
def test_fetch_resident(mock_get_resident_by_id):
    mock_get_resident_by_id.return_value = MagicMock()
    response = client.get("/fetch", params={"resident_id": 1})
    assert response.status_code == 200
    mock_get_resident_by_id.assert_called_once_with(1)
