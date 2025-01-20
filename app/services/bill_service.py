from app.database.mongo_connection import connect
from app.database.connection import get_connection

# MongoDB setup
mongo_client = connect()
mongo_db = mongo_client['smart_home']
sensor_data_collection = mongo_db['sensor_data']

def calculate_total_amount(house_id, start_date, stop_date):
    # Fetch sensor data from MongoDB
    sensor_data = sensor_data_collection.find({
        'house_id': house_id,
        'timestamp': {'$gte': start_date, '$lte': stop_date}
    })
    
    total_units = sum(data['units'] for data in sensor_data)
    total_amount = total_units * 0.3951
    
    # Store the result in MySQL
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO Bill_Info (house_id, start_date, stop_date, total_units, total_amount)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (house_id, start_date, stop_date, total_units, total_amount))
        conn.commit()
    finally:
        conn.close()
    
    return total_amount

def dump_bill_data(bill_data_request):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO Bill_Info (bill_name, bill_type, total_consumption, amount, house_id, user_id, access_level, due_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                bill_data_request.bill_name,
                bill_data_request.bill_type,
                bill_data_request.total_consumption,
                bill_data_request.amount,
                bill_data_request.house_id,
                bill_data_request.user_id,
                bill_data_request.access_level,
                bill_data_request.due_date
            ))
        conn.commit()
    finally:
        conn.close()
