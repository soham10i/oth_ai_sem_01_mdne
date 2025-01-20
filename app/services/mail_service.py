import pymysql
from app.database.connection import get_connection
from app.models.mail import UserMailCreate
from fastapi import HTTPException, status
from fastapi import Depends
from app.services.auth_service import get_current_user

def send_mail(mail: UserMailCreate):
    """
    Send a mail and insert it into the database.
    
    :param mail: UserMailCreate object containing mail details
    :return: The inserted mail object
    """
    conn = get_connection()
    try:
        # Fetch sender_id from current logged in user
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
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error sending mail: {str(e)}")
    finally:
        conn.close()

def delete_mail(mail_id: int, sender_id: int):
    """
    Delete a mail from the database.
    
    :param mail_id: ID of the mail to delete
    :param sender_id: ID of the sender
    :return: The deleted mail object
    """
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
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting mail: {str(e)}")
    finally:
        conn.close()

def get_mail(mail_id: int):
    """
    Retrieve a mail by its ID.
    
    :param mail_id: ID of the mail to retrieve
    :return: The retrieved mail object
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM User_Mail WHERE user_mail_id = %s"
            cursor.execute(sql, (mail_id,))
            mail = cursor.fetchone()
            if not mail:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail not found")
            return mail
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving mail: {str(e)}")
    finally:
        conn.close()

def get_mails_by_receiver(receiver_id: int):
    """
    Retrieve all mails for a specific receiver.
    
    :param receiver_id: ID of the receiver
    :return: List of mails for the receiver
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM User_Mail WHERE receiver_id = %s"
            cursor.execute(sql, (receiver_id,))
            mails = cursor.fetchall()
            return mails
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving mails by receiver: {str(e)}")
    finally:
        conn.close()

def get_mails_by_sender(sender_id: int):
    """
    Retrieve all mails sent by a specific sender.
    
    :param sender_id: ID of the sender
    :return: List of mails sent by the sender
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM User_Mail WHERE sender_id = %s"
            cursor.execute(sql, (sender_id,))
            mails = cursor.fetchall()
            return mails
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving mails by sender: {str(e)}")
    finally:
        conn.close()

def get_unread_mails(user_id: int, user_type: str):
    """
    Retrieve all unread mails for a specific user.
    
    :param user_id: ID of the user
    :param user_type: Type of the user (receiver_id/sender_id)
    :return: List of unread mails for the user
    """
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving unread mails: {str(e)}")
    finally:
        conn.close()
