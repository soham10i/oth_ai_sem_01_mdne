from pydantic import BaseModel
from typing import Dict

class SensorDetail(BaseModel):
    sensor_id: int
    value: float
    unit: str

class SensorDataModel(BaseModel):
    house_id: int
    sensor_data: Dict[str, SensorDetail]
    timestamp: str
