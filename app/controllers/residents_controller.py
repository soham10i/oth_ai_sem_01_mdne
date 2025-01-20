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
    return create_resident(db, resident)

@router.put("/update", response_model=ResidentResponse)
def modify_resident(resident: ResidentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_logged_in_user(current_user)
    return update_resident(db, resident)

@router.delete("/delete", response_model=ResidentResponse)
def remove_resident(resident: ResidentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_user_type(current_user, ["admin", "owner"])
    return delete_resident(db, resident)

@router.get("/house", response_model=list[ResidentResponse])
def fetch_residents(house: ResidentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_user_type(current_user, ["admin", "owner"])
    return get_residents_by_house_id(db, house.house_id)
