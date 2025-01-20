from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional
import random
import time
from bson import ObjectId
from datetime import datetime

# MongoDB settings
MONGO_URI = "mongodb://localhost:27017/"  # Local MongoDB URI, change for cloud-based MongoDB
DATABASE_NAME = "smart_home"
COLLECTION_NAME = "sensor_data"

# MongoDB client setup
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# FastAPI app initialization
app = FastAPI()

# Pydantic model for creating/updating documents
class SensorData(BaseModel):
    house_id: int
    temperature: float
    humidity: float
    pressure: float
    electricity: dict
    gas: dict
    timestamp: str

# Helper to convert ObjectId to string
def convert_oid(data):
    if isinstance(data, list):
        for doc in data:
            doc["_id"] = str(doc["_id"])
    elif isinstance(data, dict):
        data["_id"] = str(data["_id"])
    return data

# Create a document
@app.post("/create/") 
def create_document(document: SensorData):
    document_data = document.dict()
    document_data["timestamp"] = document_data.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S"))
    result = collection.insert_one(document_data)
    return {"message": "Document created", "id": str(result.inserted_id)}

# Sample request body for /create/ endpoint
"""
{
    "house_id": 1,
    "temperature": 22.5,
    "humidity": 45.0,
    "pressure": 1015.0,
    "electricity": {
        "energy_consumption": {
            "value": 3.5,
            "unit": "kWh"
        }
    },
    "gas": {
        "natural_gas_consumption": {
            "value": 2.0,
            "unit": "m^3"
        }
    },
    "timestamp": "2023-10-01 12:00:00"
}
"""

# Read documents
@app.get("/read/")   #http://127.0.0.1:8000/read/?house_id=3&start_date=2025-01-01&end_date=2025-01-31   -----> change the house_id and dates
def read_documents(
    house_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    filter_query = {}
    if house_id:
        filter_query["house_id"] = house_id
    if start_date:
        filter_query["timestamp"] = {"$gte": f"{start_date} 00:00:00"}
    if end_date:
        filter_query.setdefault("timestamp", {}).update({"$lte": f"{end_date} 23:59:59"})

    documents = list(collection.find(filter_query))
    convert_oid(documents)
    return {"data": documents}

# Fetch all sensor data using house ID
@app.get("/sensors/{house_id}")
def get_sensors_by_house_id(house_id: int):
    filter_query = {"house_id": house_id}
    documents = list(collection.find(filter_query))
    convert_oid(documents)
    return {"data": documents}

# Update documents
@app.put("/update/")
def update_document(
    house_id: int,
    update_data: dict,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    filter_query = {"house_id": house_id}
    if start_date:
        filter_query["timestamp"] = {"$gte": f"{start_date} 00:00:00"}
    if end_date:
        filter_query.setdefault("timestamp", {}).update({"$lte": f"{end_date} 23:59:59"})

    result = collection.update_many(filter_query, {"$set": update_data})
    return {"matched_count": result.matched_count, "modified_count": result.modified_count}

# Delete documents
@app.delete("/delete/")
def delete_documents(
    house_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    # Build the filter query
    filter_query = {}
    if house_id:
        filter_query["house_id"] = house_id
    if start_date:
        filter_query["timestamp"] = {"$gte": f"{start_date} 00:00:00"}
    if end_date:
        filter_query.setdefault("timestamp", {}).update({"$lte": f"{end_date} 23:59:59"})

    # Delete documents
    result = collection.delete_many(filter_query)
    return {"deleted_count": result.deleted_count}


@app.get("/")
def root():
    return {"message": "Welcome to the MongoDB CRUD API"}


# Function to add time range to filter query
def add_time_range(filter_query):
    start_date = input("Enter start date (YYYY-MM-DD) or press Enter to skip: ")
    end_date = input("Enter end date (YYYY-MM-DD) or press Enter to skip: ")

    if start_date:
        filter_query["timestamp"] = {"$gte": f"{start_date} 00:00:00"}
    if end_date:
        filter_query.setdefault("timestamp", {}).update({"$lte": f"{end_date} 23:59:59"})

    return filter_query

if __name__ == "__main__":
    while True:
        print("\nCRUD Operations on MongoDB:")
        print("1. Create a new document")
        print("2. Read documents")
        print("3. Update documents")
        print("4. Delete documents")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Example document for creation
            house_id = int(input("Enter house_id: "))
            document = {
                "house_id": house_id,
                "temperature": round(random.uniform(20.0, 25.0), 2),
                "humidity": round(random.uniform(30.0, 50.0), 2),
                "pressure": round(random.uniform(1000, 1020), 2),
                "electricity": {
                    "energy_consumption": {
                        "value": round(random.uniform(0.1, 5.0), 2),
                        "unit": "kWh"
                    }
                },
                "gas": {
                    "natural_gas_consumption": {
                        "value": round(random.uniform(0.1, 5.0), 2),
                        "unit": "m^3"
                    }
                },
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            create_document(document)
        
        elif choice == "2":
            filter_query = input("Enter filter query as a dictionary (e.g., {'house_id': 1}): ")
            try:
                filter_query = eval(filter_query) if filter_query else {}
                filter_query = add_time_range(filter_query)
                read_documents(filter_query)
            except Exception as e:
                print(f"Invalid query format: {e}")
        
        elif choice == "3":
            filter_query = input("Enter filter query as a dictionary (e.g., {'house_id': 1}): ")
            update_data = input("Enter update data as a dictionary (e.g., {'temperature': 22.5}): ")
            try:
                filter_query = eval(filter_query)
                filter_query = add_time_range(filter_query)
                update_data = eval(update_data)
                update_document(filter_query, update_data)
            except Exception as e:
                print(f"Invalid query or update data format: {e}")
        
        elif choice == "4":
            filter_query = input("Enter filter query as a dictionary (e.g., {'house_id': 1}): ")
            try:
                filter_query = eval(filter_query)
                filter_query = add_time_range(filter_query)
                delete_documents(filter_query)
            except Exception as e:
                print(f"Invalid query format: {e}")
        
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
