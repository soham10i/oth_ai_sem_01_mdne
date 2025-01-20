from fastapi.testclient import TestClient
from app.controllers.sensor_data_controller import router
from unittest.mock import patch, MagicMock

client = TestClient(router)

@patch('app.services.sensor_data_service.SensorDataService.start_scheduler')
def test_scheduler_start(mock_start_scheduler):
    mock_start_scheduler.return_value = MagicMock()
    response = client.post("/scheduler/start")
    assert response.status_code == 200
    assert response.json() == {"message": "Scheduler started successfully"}
    mock_start_scheduler.assert_called_once()

@patch('app.services.sensor_data_service.SensorDataService.stop_scheduler')
def test_scheduler_stop(mock_stop_scheduler):
    mock_stop_scheduler.return_value = MagicMock()
    response = client.post("/scheduler/stop")
    assert response.status_code == 200
    assert response.json() == {"message": "Scheduler stopped successfully"}
    mock_stop_scheduler.assert_called_once()

@patch('app.services.sensor_data_service.SensorDataService.generate_sensor_data')
def test_generate_sensor_data(mock_generate_sensor_data):
    mock_generate_sensor_data.return_value = MagicMock()
    response = client.post("/generate/1")
    assert response.status_code == 200
    mock_generate_sensor_data.assert_called_once_with(1)
