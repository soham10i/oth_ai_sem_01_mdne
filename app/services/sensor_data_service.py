import random
import schedule
import threading
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from pymongo import MongoClient
from app.database.connection import get_connection
from app.database.influxdb_connection import write_api, query_api, bucket, org
from app.database.mongo_connection import connect

class SensorDataService:
    def __init__(self):
        self.mongo_client = MongoClient("mongodb://localhost:27017/")
        self.mongo_db = self.mongo_client["smart_home"]
        self.mongo_collection = self.mongo_db["sensor_data"]
        
        self.influx_client = InfluxDBClient(url="http://localhost:8086", token="your_token", org="your_org")
        self.influx_write_api = self.influx_client.write_api()

    def generate_random_sensor_data(self):
        return {
            "temperature": {"value": round(random.uniform(15.0, 30.0), 2), "unit": "C"},
            "humidity": {"value": random.randint(30, 70), "unit": "%"},
            "pressure": {"value": random.randint(980, 1050), "unit": "hPa"},
            "electricity": {"value": round(random.uniform(1.0, 10.0), 2), "unit": "kWh"},
            "gas": {"value": round(random.uniform(0.5, 5.0), 2), "unit": "m^3"}
        }

    def generate_sensor_data(self, house_id):
        sensor_data = {
            "house_id": house_id,
            "sensor_data": self.generate_random_sensor_data(),
            "timestamp": datetime.utcnow().isoformat()
        }
        # Save to MongoDB
        self.mongo_collection.insert_one(sensor_data)
        # Save to InfluxDB
        influx_data = {
            "measurement": "sensor_data",
            "tags": {"house_id": house_id},
            "fields": sensor_data["sensor_data"],
            "time": sensor_data["timestamp"]
        }
        self.influx_write_api.write(bucket="sensor_data", record=influx_data)
    
    def start_scheduler(self):
        schedule.every(10).seconds.do(self.generate_sensor_data, house_id=1)  # Example: house_id = 1
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()
        return schedule

    def run_scheduler(self):
        while True:
            schedule.run_pending()

    def stop_scheduler(self, scheduler):
        schedule.clear()

def get_sensors():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT house_id, sensor_id, sensor_type FROM Sensors_Info")
            sensors = cursor.fetchall()
        return sensors
    finally:
        conn.close()

def fetch_all_house_ids():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT house_id FROM Sensors_Info")
            house_ids = [row['house_id'] for row in cursor.fetchall()]
        return house_ids
    finally:
        conn.close()

def generate_sensor_data(house_id, sensor_id, sensor_type):
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    value = round(random.uniform(20.0, 25.0), 2) if sensor_type == "temperature" else \
            round(random.uniform(30.0, 50.0), 2) if sensor_type == "humidity" else \
            round(random.uniform(1000, 1020), 2) if sensor_type == "pressure" else \
            round(random.uniform(0.1, 5.0), 2) if sensor_type == "electricity" else \
            round(random.uniform(0.1, 5.0), 2)
    unit = "C" if sensor_type == "temperature" else \
           "%" if sensor_type == "humidity" else \
           "hPa" if sensor_type == "pressure" else \
           "kWh" if sensor_type == "electricity" else \
           "m^3"
    sensor_data = {
        "house_id": house_id,
        "sensor_data": {
            sensor_type: {
                "sensor_id": sensor_id,
                "value": value,
                "unit": unit
            }
        },
        "timestamp": timestamp
    }
    return sensor_data

def save_to_influxdb(sensor_data):
    try:
        points = []
        for sensor_type, data in sensor_data["sensor_data"].items():
            point = Point(sensor_type) \
                .tag("house_id", sensor_data["house_id"]) \
                .tag("sensor_id", data["sensor_id"]) \
                .field("value", data["value"]) \
                .field("unit", data["unit"]) \
                .time(sensor_data["timestamp"], WritePrecision.NS)
            points.append(point)
        write_api.write(bucket=bucket, org=org, record=points)
    except Exception as e:
        print(f"Error saving to InfluxDB: {e}")

def fetch_sensor_data_from_influxdb(house_id):
    try:
        query = f'from(bucket: "{bucket}") |> range(start: -12h) |> filter(fn: (r) => r["house_id"] == "{house_id}")'
        result = query_api.query(org=org, query=query)
        
        sensor_data = {
            "house_id": house_id,
            "sensor_data": {},
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        
        for table in result:
            for record in table.records:
                sensor_type = record.get_measurement()
                sensor_data["sensor_data"][sensor_type] = {
                    "sensor_id": record["sensor_id"],
                    "value": record["_value"],
                    "unit": record["unit"]
                }
        
        return sensor_data
    except Exception as e:
        print(f"Error fetching from InfluxDB: {e}")
        return None

def generate_random_sensor_data():
    """
    Generate random sensor data with consistent types for fields.
    """
    return {
        "temperature": {
            "value": round(random.uniform(15.0, 30.0), 2),  # Float
            "unit": "C"
        },
        "humidity": {
            "value": float(random.randint(30, 70)),  # Cast to float
            "unit": "%"
        },
        "pressure": {
            "value": random.randint(980, 1050),  # Integer
            "unit": "hPa"
        },
        "electricity": {
            "value": round(random.uniform(1.0, 10.0), 2),  # Float
            "unit": "kWh"
        },
        "gas": {
            "value": round(random.uniform(0.5, 5.0), 2),  # Float
            "unit": "m^3"
        }
    }

def generate_sensor_data_for_house(house_id):
    try:
        sensors = get_sensors()
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        random_data = generate_random_sensor_data()

        sensor_data = {
            "house_id": house_id,
            "sensor_data": {
                "temperature": {
                    "sensor_id": None,
                    "value": random_data["temperature"]["value"],
                    "unit": random_data["temperature"]["unit"]
                },
                "humidity": {
                    "sensor_id": None,
                    "value": random_data["humidity"]["value"],
                    "unit": random_data["humidity"]["unit"]
                },
                "pressure": {
                    "sensor_id": None,
                    "value": random_data["pressure"]["value"],
                    "unit": random_data["pressure"]["unit"]
                },
                "electricity": {
                    "sensor_id": None,
                    "value": random_data["electricity"]["value"],
                    "unit": random_data["electricity"]["unit"]
                },
                "gas": {
                    "sensor_id": None,
                    "value": random_data["gas"]["value"],
                    "unit": random_data["gas"]["unit"]
                }
            },
            "timestamp": timestamp
        }

        for sensor in sensors:
            if sensor['house_id'] == house_id:
                sensor_type = sensor['sensor_type']
                sensor_data['sensor_data'][sensor_type]['sensor_id'] = sensor['sensor_id']
        
        save_to_influxdb(sensor_data)
        
        return sensor_data
    except Exception as e:
        print(f"Error generating sensor data for house: {e}")
        return None

def dump_sensor_data_to_influxdb(sensor_data):
    try:
        save_to_influxdb(sensor_data)
        print("Sensor data successfully dumped into InfluxDB.")
    except Exception as e:
        print(f"Error dumping sensor data into InfluxDB: {e}")

def fetch_and_store_sensor_data_in_mongo(house_id):
    try:
        sensor_data = fetch_sensor_data_from_influxdb(house_id)
        if sensor_data:
            from app.services.mongo_service import store_sensor_data_in_mongo
            store_sensor_data_in_mongo(sensor_data)
            print("Sensor data successfully stored in MongoDB.")
        else:
            print("No sensor data found in InfluxDB for the given house ID.")
    except Exception as e:
        print(f"Error fetching and storing sensor data: {e}")

def periodic_generate_sensor_data_for_house(house_id):
    try:
        sensors = get_sensors()
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        random_data = generate_random_sensor_data()

        sensor_data = {
            "house_id": house_id,
            "sensor_data": {
                "temperature": {
                    "sensor_id": None,
                    "value": random_data["temperature"]["value"],
                    "unit": random_data["temperature"]["unit"]
                },
                "humidity": {
                    "sensor_id": None,
                    "value": random_data["humidity"]["value"],
                    "unit": random_data["humidity"]["unit"]
                },
                "pressure": {
                    "sensor_id": None,
                    "value": random_data["pressure"]["value"],
                    "unit": random_data["pressure"]["unit"]
                },
                "electricity": {
                    "sensor_id": None,
                    "value": random_data["electricity"]["value"],
                    "unit": random_data["electricity"]["unit"]
                },
                "gas": {
                    "sensor_id": None,
                    "value": random_data["gas"]["value"],
                    "unit": random_data["gas"]["unit"]
                }
            },
            "timestamp": timestamp
        }

        for sensor in sensors:
            if sensor['house_id'] == house_id:
                sensor_type = sensor['sensor_type']
                sensor_data['sensor_data'][sensor_type]['sensor_id'] = sensor['sensor_id']
        
        # Save to MongoDB
        db = connect()
        db.sensor_data.insert_one(sensor_data)
        
        return sensor_data
    except Exception as e:
        print(f"Error generating sensor data for house: {e}")
        return None
