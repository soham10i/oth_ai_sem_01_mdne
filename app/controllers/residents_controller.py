"""
This module provides API endpoints for managing residents in a smart home management system.

Endpoints:
    - POST /add: Add a new resident.
    - PUT /update: Update an existing resident.
    - DELETE /delete: Delete a resident.
    - GET /house: Fetch all residents for a specific house.

Functions:
    add_resident(resident: ResidentCreate, db: Session, current_user: User): Adds a new resident.
    modify_resident(resident: ResidentCreate, db: Session, current_user: User): Updates an existing resident.
    remove_resident(resident: ResidentCreate, db: Session, current_user: User): Deletes a resident.
    fetch_residents(house: ResidentCreate, db: Session, current_user: User): Fetches all residents for a specific house.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.residents_service import create_resident, update_resident, delete_resident, get_residents_by_house_id, check_user_type, check_logged_in_user
from app.models.resident import ResidentCreate, ResidentResponse
from app.database.connection import get_db
from app.services.auth_service import get_current_user

router = APIRouter()


@router.post("/add", response_model=ResidentResponse)
def add_resident(resident: ResidentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_logged_in_user(current_user)
    try:
        return create_resident(db, resident)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/update", response_model=ResidentResponse)
def modify_resident(resident: ResidentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_logged_in_user(current_user)
    try:
        return update_resident(db, resident)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/delete", response_model=ResidentResponse)
def remove_resident(resident: ResidentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_user_type(current_user, ["admin", "owner"])
    try:
        return delete_resident(db, resident)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/house", response_model=list[ResidentResponse])
def fetch_residents(house: ResidentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_user_type(current_user, ["admin", "owner"])
    try:
        return get_residents_by_house_id(db, house.house_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
