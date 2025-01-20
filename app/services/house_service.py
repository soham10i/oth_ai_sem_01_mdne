import pymysql
from app.database.connection import get_connection
from app.models.house import HouseCreate
from fastapi import HTTPException, status

def get_house(house_id: int):
    """
    Retrieve a house by its ID.
    
    :param house_id: ID of the house to retrieve
    :return: The retrieved house object
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM houses WHERE house_id = %s"
            cursor.execute(sql, (house_id,))
            house = cursor.fetchone()
            if not house:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
            return house
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving house: {str(e)}")
    finally:
        conn.close()

def get_houses(skip: int = 0, limit: int = 10):
    """
    Retrieve a list of houses with pagination.
    
    :param skip: Number of houses to skip
    :param limit: Maximum number of houses to retrieve
    :return: List of houses
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM houses LIMIT %s OFFSET %s"
            cursor.execute(sql, (limit, skip))
            houses = cursor.fetchall()
            return houses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving houses: {str(e)}")
    finally:
        conn.close()

def get_houses_by_owner(owner_id: int):
    """
    Retrieve all houses owned by a specific owner.
    
    :param owner_id: ID of the owner
    :return: List of houses owned by the owner
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM houses WHERE owner_id = %s"
            cursor.execute(sql, (owner_id,))
            houses = cursor.fetchall()
            return houses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving houses by owner: {str(e)}")
    finally:
        conn.close()

def create_house(house: HouseCreate):
    """
    Create a new house in the database.
    
    :param house: HouseCreate object containing house details
    :return: The created house object
    """
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
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating house: {str(e)}")
    finally:
        conn.close()

def update_house(house_id: int, house: HouseCreate):
    """
    Update an existing house in the database.
    
    :param house_id: ID of the house to update
    :param house: HouseCreate object containing updated house details
    :return: The updated house object
    """
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
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating house: {str(e)}")
    finally:
        conn.close()

def delete_house(house_id: int):
    """
    Delete a house from the database.
    
    :param house_id: ID of the house to delete
    :return: The deleted house object
    """
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
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting house: {str(e)}")
    finally:
        conn.close()

def get_house_by_id(house_id: int):
    """
    Retrieve a house by its ID.
    
    :param house_id: ID of the house to retrieve
    :return: The retrieved house object
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM houses WHERE house_id = %s"
            cursor.execute(sql, (house_id,))
            house = cursor.fetchone()
            if not house:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
            return house
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving house: {str(e)}")
    finally:
        conn.close()
