import random
import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB configuration
bucket = "smart_home"
org = "smart_home_organisation"
token = "l2A12FUbNdmP19DsZD5NZJ0Jbx4_rGuuhPL1LRMVJ6F3ksTp3wyd8hx7pdRgSKI1fW6gUMysouKtqc0a6BMbxg=="
url = "http://localhost:8086"

def generate_random_sensor_data():
    """
    Generate random sensor data with consistent types for fields.
    """
    return {
        "house_id": 1,
        "sensor_data": {
            "temperature": {
                "sensor_id": 1,
                "value": round(random.uniform(15.0, 30.0), 2),  # Float
                "unit": "C"
            },
            "humidity": {
                "sensor_id": 2,
                "value": float(random.randint(30, 70)),  # Cast to float
                "unit": "%"
            },
            "pressure": {
                "sensor_id": 3,
                "value": random.randint(980, 1050),  # Integer
                "unit": "hPa"
            },
            "electricity": {
                "energy_consumption": {
                    "value": round(random.uniform(1.0, 10.0), 2),  # Float
                    "unit": "kWh"
                }
            },
            "gas": {
                "natural_gas_consumption": {
                    "value": round(random.uniform(0.5, 5.0), 2),  # Float
                    "unit": "m^3"
                }
            }
        },
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

def write_to_influxdb(data):
    """
    Write the provided sensor data to the InfluxDB bucket.
    """
    with InfluxDBClient(url=url, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        # Create a data point for InfluxDB
        point = Point("sensor_data") \
            .tag("house_id", data["house_id"]) \
            .field("temperature", data["sensor_data"]["temperature"]["value"]) \
            .field("humidity", data["sensor_data"]["humidity"]["value"]) \
            .field("pressure", data["sensor_data"]["pressure"]["value"]) \
            .field("electricity", data["sensor_data"]["electricity"]["energy_consumption"]["value"]) \
            .field("gas", data["sensor_data"]["gas"]["natural_gas_consumption"]["value"]) \
            .time(data["timestamp"], WritePrecision.NS)

        # Write the point to InfluxDB
        write_api.write(bucket=bucket, org=org, record=point)

if __name__ == "__main__":
    # Generate and write 10 random data points
    for _ in range(10):
        sensor_data = generate_random_sensor_data()
        write_to_influxdb(sensor_data)
        print(f"Written data: {sensor_data}")
