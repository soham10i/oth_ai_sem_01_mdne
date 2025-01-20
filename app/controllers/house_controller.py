


"""
This module defines the house controller for the smart home management application.
It provides endpoints for adding, fetching, updating, and deleting house records.
Endpoints:
- POST /add: Add a new house. Requires 'owner' or 'admin' user type.
- GET /fetchAll: Fetch all houses with pagination. Requires 'admin' user type.
- GET /fetch/owner: Fetch houses by owner ID. Requires 'owner' or 'admin' user type.
- PUT /update: Update house details. Requires 'admin' user type.
- DELETE /delete: Delete a house by ID. Requires 'admin' user type.
- GET /fetch: Fetch a house by ID. Requires 'owner' or 'admin' user type.
Dependencies:
- FastAPI's APIRouter for routing.
- HTTPException and status for error handling.
- Depends for dependency injection.
- SQLAlchemy's Session for database interaction.
- Custom services and models for house and user management.
Functions:
- check_user_type: Checks if the current user is an 'owner' or 'admin'.
- check_admin_user: Checks if the current user is an 'admin'.
- add_house: Adds a new house.
- fetch_all_houses: Fetches all houses with pagination.
- fetch_houses_by_owner: Fetches houses by owner ID.
- update_house_details: Updates house details.
- delete_house_details: Deletes a house by ID.
- fetch_house: Fetches a house by ID.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models.house import HouseCreate, HouseResponse
from app.services.house_service import create_house, get_houses, get_houses_by_owner, update_house, delete_house, get_house_by_id
from app.database.connection import get_db
from sqlalchemy.orm import Session
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter()

def check_user_type(current_user: User):
    if current_user.user_type not in ['owner', 'admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")

def check_admin_user(current_user: User):
    if current_user.user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only admin can perform this action")

@router.post("/add", response_model=HouseResponse, status_code=status.HTTP_201_CREATED)
def add_house(house: HouseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_user_type(current_user)
    db_house = create_house(house)
    if not db_house:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="House could not be created")
    return db_house

@router.get("/fetchAll", response_model=List[HouseResponse])
def fetch_all_houses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin_user(current_user)
    houses = get_houses(skip=skip, limit=limit)
    return houses

@router.get("/fetch/owner", response_model=List[HouseResponse])
def fetch_houses_by_owner(owner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_user_type(current_user)
    houses = get_houses_by_owner(owner_id)
    return houses

@router.put("/update", response_model=HouseResponse)
def update_house_details(house: HouseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin_user(current_user)
    db_house = update_house(db, house)
    if not db_house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
    return db_house

@router.delete("/delete", response_model=HouseResponse)
def delete_house_details(house_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin_user(current_user)
    db_house = delete_house(db, house_id)
    if not db_house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
    return db_house

@router.get("/fetch", response_model=HouseResponse)
def fetch_house(house_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_user_type(current_user)
    db_house = get_house_by_id(db, house_id)
    if not db_house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
    return db_house
