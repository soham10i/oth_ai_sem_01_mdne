from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, UserResponse, UserCreate
from app.services.user_service import get_user_by_id, update_user_by_id, delete_user_by_id, get_all_users
from app.services.auth_service import get_current_user, access_level_required
from app.database.connection import get_db
from typing import List

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
def get_current_user_details(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        user = get_user_by_id(db, current_user.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update", response_model=UserResponse)
def update_current_user(user_update: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        updated_user = update_user_by_id(db, current_user.user_id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete", response_model=UserResponse)
@access_level_required('admin')
def delete_current_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        deleted_user = delete_user_by_id(db, current_user.user_id)
        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found")
        return deleted_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", response_model=List[UserResponse])
@access_level_required('admin')
def fetch_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        users = get_all_users(db)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
