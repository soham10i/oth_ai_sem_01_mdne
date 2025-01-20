# Smart Home Management

## Implementation Steps

### Using Docker

1. Ensure Docker and Docker Compose are installed on your system.
2. Navigate to the project directory.
3. Build and start the containers:
   ```sh
   docker-compose up --build
   ```
4. Access the application at `http://localhost:8000`.

### On Windows

1. Ensure Python 3.10.9 is installed.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the application:
   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
4. Access the application at `http://localhost:8000`.

### On macOS

1. Ensure Python 3.10.9 is installed.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the application:
   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
4. Access the application at `http://localhost:8000`.

### On Linux

1. Ensure Python 3.10.9 is installed.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the application:
   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
4. Access the application at `http://localhost:8000`.

## Modules

### Sensor Data Module

This module handles the collection and storage of sensor data from various sensors in the smart home.

### User Management Module

This module manages user authentication and authorization.

### Device Control Module

This module allows users to control various smart devices in their home.

## Endpoints

### Get Sensor Data

- **URL:** `/sensor_data`
- **Method:** `GET`
- **Request Body:** None
- **Response:**
  ```json
  {
      "house_id": 1,
      "sensor_data": {
          "temperature": {
              "sensor_id": 1,
              "value": 22.5,
              "unit": "C"
          },
          "humidity": {
              "sensor_id": 2,
              "value": 50,
              "unit": "%"
          },
          "pressure": {
              "sensor_id": 3,
              "value": 1013,
              "unit": "hPa"
          },
          "electricity": {
              "sensor_id": 4,
              "value": 3.5,
              "unit": "kWh"
          },
          "gas": {
              "sensor_id": 5,
              "value": 2,
              "unit": "m3"
          }
      },
      "timestamp": "2023-10-01 12:00:00"
  }
  ```

### Add Sensor Data

- **URL:** `/sensor_data`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "house_id": 2,
      "sensor_data": {
          "temperature": {
              "sensor_id": 1,
              "value": 27.18,
              "unit": "C"
          },
          "humidity": {
              "sensor_id": 2,
              "value": 55,
              "unit": "%"
          },
          "pressure": {
              "sensor_id": 3,
              "value": 1014,
              "unit": "hPa"
          },
          "electricity": {
              "sensor_id": 4,
              "value": 7.08,
              "unit": "kWh"
          },
          "gas": {
              "sensor_id": 5,
              "value": 1.95,
              "unit": "m^3"
          }
      },
      "timestamp": "2025-01-20T12:59:01Z"
  }
  ```
- **Response:**
  ```json
  {
      "message": "Sensor data added successfully"
  }
  ```

### User Registration

- **URL:** `/register`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "username": "user1",
      "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
      "message": "User registered successfully"
  }
  ```

### User Login

- **URL:** `/login`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "username": "user1",
      "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
      "access_token": "jwt_token",
      "token_type": "bearer"
  }
  ```

### Control Device

- **URL:** `/device_control`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "device_id": 1,
      "action": "turn_on"
  }
  ```
- **Response:**
  ```json
  {
      "message": "Device turned on successfully"
  }
  ```

// ...additional endpoints...
