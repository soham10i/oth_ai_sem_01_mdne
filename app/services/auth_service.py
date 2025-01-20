from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User, UserCreate
from datetime import datetime, timedelta
import jwt
from functools import wraps
from fastapi import HTTPException, status
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database.connection import get_db

SECRET_KEY = "441c876eba4beb1ea06d31cb48f4c03f4cfbb96fff97114fe48ca5cc5516f67b"  # Replace with your generated secret key
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.
    
    :param db: Database session
    :param user: UserCreate object containing user details
    :return: Created User object
    """
    try:
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            dob=user.dob,
            email=user.email,
            password=hashed_password,
            user_type=user.user_type.lower()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by email from the database.
    
    :param db: Database session
    :param email: User's email
    :return: User object or None
    """
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user by email: {str(e)}")

def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user by email and password.
    
    :param db: Database session
    :param email: User's email
    :param password: User's password
    :return: User object if authentication is successful, False otherwise
    """
    try:
        user = get_user_by_email(db, email)
        if not user:
            return False
        if not pwd_context.verify(password, user.password):
            return False
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error authenticating user: {str(e)}")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=24)):
    """
    Create a new access token.
    
    :param data: Data to encode in the token
    :param expires_delta: Token expiration time
    :return: Encoded JWT token
    """
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating access token: {str(e)}")

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    """
    Create a new refresh token.
    
    :param data: Data to encode in the token
    :param expires_delta: Token expiration time
    :return: Encoded JWT token
    """
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating refresh token: {str(e)}")

def restrict_access(user, required_access_level):
    """
    Restrict user access to certain API endpoints or methods based on access level.
    
    :param user: The user object
    :param required_access_level: The required access level for the endpoint/method
    :return: Boolean indicating if access is granted or not
    """
    user_access_level = user.access_level  # Assuming user object has an access_level attribute
    
    access_levels = ['private', 'restricted', 'public']
    
    if access_levels.index(user_access_level) >= access_levels.index(required_access_level):
        return True
    return False

def access_level_required(required_access_level):
    """
    Decorator to enforce access level restrictions on API endpoints or methods.
    
    :param required_access_level: The required access level for the endpoint/method
    :return: Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('user')
            if not user or not restrict_access(user, required_access_level):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access forbidden: insufficient access level"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Retrieve the current authenticated user based on the provided token.
    
    :param db: Database session
    :param token: JWT token
    :return: User object
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving current user: {str(e)}")
