from sqlalchemy.orm import Session
from app.models.resident import Resident, ResidentCreate, ResidentResponse
from fastapi import HTTPException, status
from app.models.user import User

def create_resident(db: Session, resident: ResidentCreate):
    db_resident = db.query(Resident).filter(Resident.house_id == resident.house_id, Resident.user_id == resident.user_id).first()
    if db_resident:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resident already exists")
    new_resident = Resident(**resident.dict())
    db.add(new_resident)
    db.commit()
    db.refresh(new_resident)
    return new_resident

def update_resident(db: Session, resident: ResidentCreate):
    db_resident = db.query(Resident).filter(Resident.resident_id == resident.resident_id).first()
    if not db_resident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resident not found")
    for key, value in resident.dict().items():
        setattr(db_resident, key, value)
    db.commit()
    db.refresh(db_resident)
    return db_resident

def delete_resident(db: Session, resident: ResidentCreate):
    db_resident = db.query(Resident).filter(Resident.resident_id == resident.resident_id).first()
    if not db_resident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resident not found")
    db.delete(db_resident)
    db.commit()
    return db_resident

def get_residents_by_house_id(db: Session, house_id: int):
    return db.query(Resident).filter(Resident.house_id == house_id).all()

def check_user_type(current_user: User, allowed_roles: list):
    if current_user.user_type not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

def check_logged_in_user(current_user: User):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

