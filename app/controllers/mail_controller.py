"""
Mail Controller
This module provides endpoints for managing user mails in the Smart Home Management application.
Endpoints:
- POST /send: Send a new mail.
- DELETE /delete/{mail_id}: Delete a mail by its ID.
- GET /fetch/{mail_id}: Fetch details of a mail by its ID.
- GET /fetch/receiver/{receiver_id}: Fetch all mails received by a specific user.
- GET /fetch/sender/{sender_id}: Fetch all mails sent by a specific user.
- GET /fetch/unread/receiver: Fetch all unread mails received by the current user.
- GET /fetch/unread/sender: Fetch all unread mails sent by the current user.
Dependencies:
- FastAPI's APIRouter for routing.
- SQLAlchemy's Session for database interactions.
- Authentication service to get the current user.
Models:
- UserMailCreate: Schema for creating a new mail.
- UserMailResponse: Schema for mail response.
- User: Schema for user details.
Services:
- send_mail: Service to send a mail.
- delete_mail: Service to delete a mail.
- get_mail: Service to get mail details.
- get_mails_by_receiver: Service to get mails by receiver.
- get_mails_by_sender: Service to get mails by sender.
- get_unread_mails: Service to get unread mails.
Database:
- get_db: Dependency to get the database session.
"""


from fastapi import APIRouter, HTTPException, status, Depends
from app.models.mail import UserMailCreate, UserMailResponse
from app.services.mail_service import send_mail, delete_mail, get_mail, get_mails_by_receiver, get_mails_by_sender, get_unread_mails
from app.database.connection import get_db
from sqlalchemy.orm import Session
from app.services.auth_service import get_current_user
from app.models.user import User
from typing import List

router = APIRouter()

@router.post("/send", response_model=UserMailResponse, status_code=status.HTTP_201_CREATED)
def send_user_mail(mail: UserMailCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    mail.sender_id = current_user.user_id
    db_mail = send_mail(mail)
    if not db_mail:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mail could not be sent")
    return db_mail

@router.delete("/delete/{mail_id}", response_model=UserMailResponse)
def delete_user_mail(mail_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_mail = delete_mail(mail_id, current_user.user_id)
    if not db_mail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail not found")
    return db_mail

@router.get("/fetch/{mail_id}", response_model=UserMailResponse)
def fetch_mail_details(mail_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_mail = get_mail(mail_id)
    if not db_mail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail not found")
    if db_mail['sender_id'] != current_user.user_id and db_mail['receiver_id'] != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return db_mail

@router.get("/fetch/receiver/{receiver_id}", response_model=List[UserMailResponse])
def fetch_mails_by_receiver(receiver_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if receiver_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    mails = get_mails_by_receiver(receiver_id)
    return mails

@router.get("/fetch/sender/{sender_id}", response_model=List[UserMailResponse])
def fetch_mails_by_sender(sender_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if sender_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    mails = get_mails_by_sender(sender_id)
    return mails

@router.get("/fetch/unread/receiver", response_model=List[UserMailResponse])
def fetch_unread_mails_receiver(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    unread_received_mails = get_unread_mails(current_user.user_id, "receiver_id")
    return unread_received_mails

@router.get("/fetch/unread/sender", response_model=List[UserMailResponse])
def fetch_unread_mails_sender(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    unread_sent_mails = get_unread_mails(current_user.user_id, "sender_id")
    return unread_sent_mails

