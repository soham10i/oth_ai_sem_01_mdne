import pytest
from fastapi.testclient import TestClient
from app.controllers.house_controller import router
from app.models.house import HouseCreate
from unittest.mock import patch, MagicMock

client = TestClient(router)

@patch('app.services.house_service.create_house')
def test_add_house(mock_create_house):
    mock_create_house.return_value = MagicMock()
    house_data = {
        "name": "Test House",
        "address": "123 Test St",
        "owner_id": 1
    }
    response = client.post("/add", json=house_data)
    assert response.status_code == 201
    mock_create_house.assert_called_once()

@patch('app.services.house_service.get_houses')
def test_fetch_all_houses(mock_get_houses):
    mock_get_houses.return_value = [MagicMock()]
    response = client.get("/fetchAll")
    assert response.status_code == 200
    mock_get_houses.assert_called_once()

@patch('app.services.house_service.get_houses_by_owner')
def test_fetch_houses_by_owner(mock_get_houses_by_owner):
    mock_get_houses_by_owner.return_value = [MagicMock()]
    response = client.get("/fetch/owner", params={"owner_id": 1})
    assert response.status_code == 200
    mock_get_houses_by_owner.assert_called_once_with(1)

@patch('app.services.house_service.update_house')
def test_update_house_details(mock_update_house):
    mock_update_house.return_value = MagicMock()
    house_data = {
        "name": "Updated House",
        "address": "123 Updated St",
        "owner_id": 1
    }
    response = client.put("/update", json=house_data)
    assert response.status_code == 200
    mock_update_house.assert_called_once()

@patch('app.services.house_service.delete_house')
def test_delete_house_details(mock_delete_house):
    mock_delete_house.return_value = MagicMock()
    response = client.delete("/delete", params={"house_id": 1})
    assert response.status_code == 200
    mock_delete_house.assert_called_once_with(1)

@patch('app.services.house_service.get_house_by_id')
def test_fetch_house(mock_get_house_by_id):
    mock_get_house_by_id.return_value = MagicMock()
    response = client.get("/fetch", params={"house_id": 1})
    assert response.status_code == 200
    mock_get_house_by_id.assert_called_once_with(1)
