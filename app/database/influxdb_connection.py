from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB configuration
bucket = "smart_home"
org = "smart_home_organisation"
token = "l2A12FUbNdmP19DsZD5NZJ0Jbx4_rGuuhPL1LRMVJ6F3ksTp3wyd8hx7pdRgSKI1fW6gUMysouKtqc0a6BMbxg=="
url = "http://localhost:8086"

# Initialize InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
