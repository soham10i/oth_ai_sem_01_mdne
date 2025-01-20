from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime, time, timedelta
from typing import Optional

import schedule
from app.services.sensor_data_service import periodic_generate_sensor_data_for_house

# MongoDB settings
MONGO_URI = "mongodb://localhost:27017/"  # Local MongoDB URI, change for cloud-based MongoDB
DATABASE_NAME = "mdne"
COLLECTION_NAME = "bill_data"

# MongoDB client setup
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# FastAPI app initialization
app = FastAPI()

# Function to calculate total sums of sensor values for a specific house_id and time range
def calculate_total_sums(house_id: int, start_date: str, end_date: str):
    filter_query = {
        "house_id": house_id,
        "timestamp": {"$gte": f"{start_date} 00:00:00", "$lte": f"{end_date} 23:59:59"}
    }
    documents = collection.find(filter_query)

    total_temperature = 0
    total_humidity = 0
    total_pressure = 0
    total_energy_consumption = 0
    total_gas_consumption = 0

    for doc in documents:
        total_temperature += doc.get("temperature", 0)
        total_humidity += doc.get("humidity", 0)
        total_pressure += doc.get("pressure", 0)
        total_energy_consumption += doc.get("electricity", {}).get("energy_consumption", {}).get("value", 0)
        total_gas_consumption += doc.get("gas", {}).get("natural_gas_consumption", {}).get("value", 0)

    return {
        "total_temperature": total_temperature,
        "total_humidity": total_humidity,
        "total_pressure": total_pressure,
        "total_energy_consumption": total_energy_consumption,
        "total_gas_consumption": total_gas_consumption
    }

@app.get("/calculate_sums/") # {calculate_sums/?house_id=2&start_date=2025-01-01&end_date=2025-01-31} -----> change the house_id and dates
def calculate_sums_api(
    house_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    try:
        # Default time range: last 10 days
        if not start_date or not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

        totals = calculate_total_sums(house_id, start_date, end_date)
        return {"house_id": house_id, "start_date": start_date, "end_date": end_date, "totals": totals}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ten_day_summary/")
def ten_day_summary_api():
    try:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

        house_ids = collection.distinct("house_id")
        results = {}

        for house_id in house_ids:
            results[house_id] = calculate_total_sums(house_id, start_date, end_date)

        return {"start_date": start_date, "end_date": end_date, "summary": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Welcome to the Smart Home API!"}

# Function to generate sensor data periodically
def generate_sensor_data_periodically():
    house_ids = [1, 2, 3]  # Example house IDs, replace with actual IDs
    for house_id in house_ids:
        periodic_generate_sensor_data_for_house(house_id)

# Schedule the periodic generation of sensor data
schedule.every(10).seconds.do(generate_sensor_data_periodically)  # Adjust the interval as needed

if __name__ == "__main__":
    while True:
        print("\nSensor Value Summation Options:")
        print("1. Calculate sum for a specific house_id and month")
        print("2. Enable automatic 10-day summary calculation")
        print("3. Exit") 

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                house_id = int(input("Enter the house_id: "))
                month = input("Enter the month in YYYY-MM format: ")
                start_date = f"{month}-01"
                end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=31)).replace(day=1) - timedelta(days=1)
                end_date = end_date.strftime("%Y-%m-%d")

                totals = calculate_total_sums(house_id, start_date, end_date)
                print(f"Total sensor values for house_id {house_id} ({start_date} to {end_date}):")
                for key, value in totals.items():
                    print(f"  {key}: {value}")
            except ValueError:
                print("Invalid input. Please enter a numeric house_id and a valid month.")

        elif choice == "2":
            print("Enabling automatic 10-day summary calculation and periodic sensor data generation...")
            schedule.every(10).seconds.do(ten_day_summary_api)  # Run every 10 seconds for testing 10-day summary
            schedule.every(10).seconds.do(generate_sensor_data_periodically)  # Run every 10 seconds for testing

            print("Scheduled checks for 10-day summary and periodic sensor data generation. Running in the background...")

            try:
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Stopping the scheduler.")

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
