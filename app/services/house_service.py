import pymysql
from app.database.connection import get_connection
from app.models.house import HouseCreate
from fastapi import HTTPException, status

def get_house(house_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM houses WHERE house_id = %s"
            cursor.execute(sql, (house_id,))
            house = cursor.fetchone()
            return house
    finally:
        conn.close()

def get_houses(skip: int = 0, limit: int = 10):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM houses LIMIT %s OFFSET %s"
            cursor.execute(sql, (limit, skip))
            houses = cursor.fetchall()
            return houses
    finally:
        conn.close()

def get_houses_by_owner(owner_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM houses WHERE owner_id = %s"
            cursor.execute(sql, (owner_id,))
            houses = cursor.fetchall()
            return houses
    finally:
        conn.close()

def create_house(house: HouseCreate):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO houses (house_name, address, owner_id)
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (house.house_name, house.address, house.owner_id))
        conn.commit()
        house_id = cursor.lastrowid
        return get_house(house_id)
    finally:
        conn.close()

def update_house(house_id: int, house: HouseCreate):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            UPDATE houses
            SET house_name = %s, address = %s, owner_id = %s
            WHERE house_id = %s
            """
            cursor.execute(sql, (house.house_name, house.address, house.owner_id, house_id))
        conn.commit()
        return get_house(house_id)
    finally:
        conn.close()

def delete_house(house_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            house = get_house(house_id)
            if not house:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
            sql = "DELETE FROM houses WHERE house_id = %s"
            cursor.execute(sql, (house_id,))
        conn.commit()
        return house
    finally:
        conn.close()

def get_house_by_id(house_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM houses WHERE house_id = %s"
            cursor.execute(sql, (house_id,))
            house = cursor.fetchone()
            if not house:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
            return house
    finally:
        conn.close()
