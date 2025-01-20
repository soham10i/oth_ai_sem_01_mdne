import pymysql
from app.database.connection import get_connection
from app.models.sensor import SensorCreate
from fastapi import HTTPException, status

def add_sensor(sensor: SensorCreate):
    """
    Add a new sensor to the database.
    
    :param sensor: SensorCreate object containing sensor details
    :return: The added sensor object
    """
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
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding sensor: {str(e)}")
    finally:
        conn.close()

def update_sensor(sensor_id: int, sensor: SensorCreate):
    """
    Update an existing sensor in the database.
    
    :param sensor_id: ID of the sensor to update
    :param sensor: SensorCreate object containing updated sensor details
    :return: The updated sensor object
    """
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
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating sensor: {str(e)}")
    finally:
        conn.close()

def delete_sensor(sensor_id: int):
    """
    Delete a sensor from the database.
    
    :param sensor_id: ID of the sensor to delete
    :return: The deleted sensor object
    """
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
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting sensor: {str(e)}")
    finally:
        conn.close()

def get_sensor(sensor_id: int):
    """
    Retrieve a sensor by its ID.
    
    :param sensor_id: ID of the sensor to retrieve
    :return: The retrieved sensor object
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM Sensors_Info WHERE sensor_id = %s"
            cursor.execute(sql, (sensor_id,))
            sensor = cursor.fetchone()
            if not sensor:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
            return sensor
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sensor: {str(e)}")
    finally:
        conn.close()

def get_sensors_by_house(house_id: int):
    """
    Retrieve all sensors for a specific house.
    
    :param house_id: ID of the house
    :return: List of sensors for the house
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM Sensors_Info WHERE house_id = %s"
            cursor.execute(sql, (house_id,))
            sensors = cursor.fetchall()
            return sensors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sensors by house: {str(e)}")
    finally:
        conn.close()
