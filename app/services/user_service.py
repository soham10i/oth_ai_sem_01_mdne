from sqlalchemy.orm import Session
from app.models.user import User, UserCreate

def get_user_by_id(db: Session, user_id: int):
    try:
        return db.query(User).filter(User.user_id == user_id).first()
    except Exception as e:
        raise e

def update_user_by_id(db: Session, user_id: int, user_update: UserCreate):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None
        for key, value in user_update.dict().items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e

def delete_user_by_id(db: Session, user_id: int):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None
        db.delete(user)
        db.commit()
        return user
    except Exception as e:
        db.rollback()
        raise e

def get_all_users(db: Session):
    try:
        return db.query(User).all()
    except Exception as e:
        raise e
