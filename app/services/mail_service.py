import pymysql
from app.database.connection import get_connection
from app.models.mail import UserMailCreate
from fastapi import HTTPException, status
from fastapi import Depends
from app.services.auth_service import get_current_user

def send_mail(mail: UserMailCreate):
    conn = get_connection()
    try:
        #fetch sender_id from current logged in user
        current_user = Depends(get_current_user)
        mail.sender_id = current_user.user_id
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO User_Mail (sender_id, receiver_id, mail_access_level, subject, message, mail_status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (mail.sender_id, mail.receiver_id, mail.mail_access_level, mail.subject, mail.message, mail.mail_status))
        conn.commit()
        mail_id = cursor.lastrowid
        return get_mail(mail_id)
    finally:
        conn.close()

def delete_mail(mail_id: int, sender_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM User_Mail WHERE user_mail_id = %s AND sender_id = %s"
            cursor.execute(sql, (mail_id, sender_id))
            mail = cursor.fetchone()
            if not mail:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail not found")
            sql = "DELETE FROM User_Mail WHERE user_mail_id = %s"
            cursor.execute(sql, (mail_id,))
        conn.commit()
        return mail
    finally:
        conn.close()

def get_mail(mail_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM User_Mail WHERE user_mail_id = %s"
            cursor.execute(sql, (mail_id,))
            mail = cursor.fetchone()
            return mail
    finally:
        conn.close()

def get_mails_by_receiver(receiver_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM User_Mail WHERE receiver_id = %s"
            cursor.execute(sql, (receiver_id,))
            mails = cursor.fetchall()
            return mails
    finally:
        conn.close()

def get_mails_by_sender(sender_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM User_Mail WHERE sender_id = %s"
            cursor.execute(sql, (sender_id,))
            mails = cursor.fetchall()
            return mails
    finally:
        conn.close()

def get_unread_mails(user_id: int, user_type: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if user_type == "receiver_id":
                sql = "SELECT * FROM User_Mail WHERE receiver_id = %s AND mail_status = 'unread'"
            elif user_type == "sender_id":
                sql = "SELECT * FROM User_Mail WHERE sender_id = %s AND mail_status = 'unread'"
            cursor.execute(sql, (user_id,))
            mails = cursor.fetchall()
            return mails
    finally:
        conn.close()
