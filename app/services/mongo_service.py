import logging
from mongoengine import Document, IntField, FloatField, StringField, DictField
from app.services.sensor_data_service import fetch_sensor_data_from_influxdb
from app.database.mongo_connection import connect
from app.database.influxdb_connection import query_api, bucket, org
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SensorDetail(Document):
    sensor_id = IntField(required=True)
    value = FloatField(required=True)
    unit = StringField(required=True)

class SensorData(Document):
    house_id = IntField(required=True)
    sensor_data = DictField(required=True)
    timestamp = StringField(required=True)

mongo_client = connect()
mongo_db = mongo_client['smart_home']
sensor_data_collection = mongo_db['sensor_data']

def fetch_and_store_sensor_data(house_id):
    sensor_data = fetch_sensor_data_from_influxdb(house_id)
    sensor_data_document = SensorData(
        house_id=sensor_data["house_id"],
        sensor_data=sensor_data["sensor_data"],
        timestamp=sensor_data["timestamp"]
    )
    sensor_data_document.save()

def store_sensor_data_in_mongo(sensor_data):
    try:
        sensor_data_collection.insert_one(sensor_data)
        logger.info(f"Inserted sensor data into MongoDB: {sensor_data}")
    except Exception as e:
        logger.error(f"Error inserting sensor data into MongoDB: {e}")

def store_all_influxdb_data_in_mongo():
    try:
        # Check MongoDB connection
        logger.info("MongoDB connection successful")
        
        query = f'from(bucket: "{bucket}") |> range(start: -12h)'
        result = query_api.query(org=org, query=query)
        
        for table in result:
            for record in table.records:
                try:
                    sensor_data = {
                        "house_id": record["house_id"],
                        "sensor_data": {
                            record.get_measurement(): {
                                "sensor_id": record["sensor_id"],
                                "value": record["_value"],
                                "unit": record["unit"]
                            }
                        },
                        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    }
                    logger.info(f"Fetched sensor data from InfluxDB: {sensor_data}")
                    print(f"Fetched sensor data from InfluxDB: {sensor_data}")
                    store_sensor_data_in_mongo(sensor_data)
                except KeyError as e:
                    logger.error(f"KeyError: {e} in record: {record}")
    except Exception as e:
        logger.error(f"Error storing all InfluxDB data in MongoDB: {e}")

def fetch_and_store_sensor_data_in_mongo(house_id):
    sensor_data = fetch_sensor_data_from_influxdb(house_id)
    if sensor_data:
        store_sensor_data_in_mongo(sensor_data)

def fetch_sensor_data_by_house_id(house_id: int):
    return SensorData.objects(house_id=house_id).all()

def fetch_sensor_data_by_sensor_id(sensor_id: int):
    return SensorData.objects(sensor_data__sensor_id=sensor_id).first()

