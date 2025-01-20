# config.py

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "adminadmin"  # URL-encoded password
MYSQL_DB = "smart_home"

# If using MongoDB for sensor metadata:
MONGO_URI = "mongodb://localhost:27017"
MONGO_DB_NAME = "mdne"  

# If using a time-series DB (e.g., InfluxDB):
TIMESERIES_DB_URL = "http://localhost:8086"
TIMESERIES_DB_TOKEN = "UKsncsOKeMVkxYII2X_K_pWqoKM_c1euKunlEnjBFyok0ysSQsgx9Ch6VuL-YJiX2D4BY4GkfjRaHKQ3Kaafkg=="
TIMESERIES_DB_ORG = "my-org"
TIMESERIES_DB_BUCKET = "sensor_data_bucket"
