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
