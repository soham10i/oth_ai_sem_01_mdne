import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.controllers.sensor_data_controller import generate_sensor_data_periodically
from app.services.sensor_data_service import get_sensors, generate_sensor_data_for_house

@patch('app.services.sensor_data_service.get_sensors')
@patch('app.services.sensor_data_service.generate_sensor_data_for_house')
def test_generate_sensor_data_periodically(mock_generate_sensor_data_for_house, mock_get_sensors):
    # Mock the return value of get_sensors
    mock_get_sensors.return_value = [
        {'house_id': 1, 'sensor_id': 1, 'sensor_type': 'temperature'},
        {'house_id': 2, 'sensor_id': 2, 'sensor_type': 'humidity'}
    ]
    
    # Call the function
    generate_sensor_data_periodically()
    
    # Assert that get_sensors was called once
    mock_get_sensors.assert_called_once()
    
    # Assert that generate_sensor_data_for_house was called for each sensor
    assert mock_generate_sensor_data_for_house.call_count == 2
    mock_generate_sensor_data_for_house.assert_any_call(1)
    mock_generate_sensor_data_for_house.assert_any_call(2)
