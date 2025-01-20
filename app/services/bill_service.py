from app.database.mongo_connection import connect
from app.database.connection import get_connection
from datetime import datetime, timedelta
from typing import List, Optional
from app.models.bill_info import BillInfo
import schedule
import threading
import time

class BillService:
    def __init__(self):
        # MongoDB Connection
        self.mongo_client = connect()
        self.sensor_data_collection = self.mongo_client["sensor_data"]

        # MySQL Connection
        self.mysql_conn = get_connection()

    def calculate_total_consumption(self):
        # Fetch all sensor data from MongoDB
        sensor_data = self.sensor_data_collection.find()

        # Consumption data
        total_consumption = {}

        # Process each document
        for data in sensor_data:
            house_id = data["house_id"]
            electricity = data["sensor_data"]["electricity"]["value"]
            gas = data["sensor_data"]["gas"]["value"]

            if house_id not in total_consumption:
                total_consumption[house_id] = {"electricity": 0.0, "gas": 0.0}

            total_consumption[house_id]["electricity"] += electricity
            total_consumption[house_id]["gas"] += gas

        return total_consumption

    def calculate_and_insert_bills(self):
        consumption_data = self.calculate_total_consumption()

        # Define rates for electricity and gas
        electricity_rate = 0.39  # per kWh
        gas_rate = 0.10  # per m3

        for house_id, consumption in consumption_data.items():
            total_electricity = consumption["electricity"]
            total_gas = consumption["gas"]

            electricity_amount = round(total_electricity * electricity_rate, 2)
            gas_amount = round(total_gas * gas_rate, 2)

            # Insert Electricity Bill
            self.insert_bill(
                bill_name="Electricity Bill",
                bill_type="electricity",
                total_consumption=total_electricity,
                amount=electricity_amount,
                house_id=house_id,
                due_date=datetime.now() + timedelta(days=30)
            )

            # Insert Gas Bill
            self.insert_bill(
                bill_name="Gas Bill",
                bill_type="gas",
                total_consumption=total_gas,
                amount=gas_amount,
                house_id=house_id,
                due_date=datetime.now() + timedelta(days=30)
            )

    def insert_bill(self, bill_name, bill_type, total_consumption, amount, house_id, due_date):
        sql = """
        INSERT INTO Bill_Info (bill_name, bill_type, total_consumption, amount, house_id, user_id, due_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        user_id = self.get_user_id(house_id)  # Assume function exists to get user_id for house_id
        conn = self.mysql_conn
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (bill_name, bill_type, total_consumption, amount, house_id, user_id, due_date))
            conn.commit()
        finally:
            conn.close()

    def get_user_id(self, house_id):
        sql = "SELECT owner_id FROM Houses WHERE house_id = %s"
        conn = self.mysql_conn
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (house_id,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    raise ValueError(f"No user found for house_id {house_id}")
        finally:
            conn.close()

    def fetch_all_bills(self, house_id: Optional[int] = None, user_id: Optional[int] = None) -> List[BillInfo]:
        sql = "SELECT * FROM Bill_Info WHERE 1=1"
        params = []

        if house_id is not None:
            sql += " AND house_id = %s"
            params.append(house_id)

        if user_id is not None:
            sql += " AND user_id = %s"
            params.append(user_id)

        conn = self.mysql_conn
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                bills = cursor.fetchall()
                return [BillInfo(**bill) for bill in bills]
        finally:
            conn.close()

    def start_monthly_scheduler(self):
        schedule.every().month.at("23:59").do(self.calculate_and_insert_bills)
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
