FROM python:3.10.9-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Wait for MySQL, MongoDB, and InfluxDB to be ready
CMD ["sh", "-c", "while ! nc -z mysql_db 3306; do sleep 1; done; \
                   while ! nc -z mongo_db 27017; do sleep 1; done; \
                   while ! nc -z influxdb 8086; do sleep 1; done; \
                   uvicorn app.main:app --host 0.0.0.0 --port 8000"]
