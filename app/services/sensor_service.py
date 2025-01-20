import pymysql
from app.database.connection import get_connection
from app.models.sensor import SensorCreate
from fastapi import HTTPException, status

def add_sensor(sensor: SensorCreate):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO Sensors_Info (sensor_name, sensor_type, sensor_manufacturer, house_id, sensor_unit)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (sensor.sensor_name, sensor.sensor_type, sensor.sensor_manufacturer, sensor.house_id, sensor.sensor_unit))
        conn.commit()
        sensor_id = cursor.lastrowid
        return get_sensor(sensor_id)
    finally:
        conn.close()

def update_sensor(sensor_id: int, sensor: SensorCreate):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            UPDATE Sensors_Info
            SET sensor_name = %s, sensor_type = %s, sensor_manufacturer = %s, house_id = %s, sensor_unit = %s
            WHERE sensor_id = %s
            """
            cursor.execute(sql, (sensor.sensor_name, sensor.sensor_type, sensor.sensor_manufacturer, sensor.house_id, sensor.sensor_unit, sensor_id))
        conn.commit()
        return get_sensor(sensor_id)
    finally:
        conn.close()

def delete_sensor(sensor_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sensor = get_sensor(sensor_id)
            if not sensor:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
            sql = "DELETE FROM Sensors_Info WHERE sensor_id = %s"
            cursor.execute(sql, (sensor_id,))
        conn.commit()
        return sensor
    finally:
        conn.close()

def get_sensor(sensor_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM Sensors_Info WHERE sensor_id = %s"
            cursor.execute(sql, (sensor_id,))
            sensor = cursor.fetchone()
            return sensor
    finally:
        conn.close()

def get_sensors_by_house(house_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM Sensors_Info WHERE house_id = %s"
            cursor.execute(sql, (house_id,))
            sensors = cursor.fetchall()
            return sensors
    finally:
        conn.close()
