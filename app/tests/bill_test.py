import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.controllers.bill_controller import router
from unittest.mock import patch, MagicMock

client = TestClient(router)

@patch('app.services.bill_service.BillService.calculate_and_insert_bills')
def test_calculate_and_insert_bills(mock_calculate_and_insert_bills):
    mock_calculate_and_insert_bills.return_value = MagicMock()
    response = client.post("/calculate_and_insert_bills")
    assert response.status_code == 200
    assert response.json() == {"message": "Bills calculated and inserted successfully"}
    mock_calculate_and_insert_bills.assert_called_once()
