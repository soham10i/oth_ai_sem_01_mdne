import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import (
    MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
)



def get_connection():
    """
    Returns a PyMySQL connection object.
    """
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

def create_tables():
    """
    Creates the required tables according to your schema.
    """
    TABLES = [
        """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            firstname VARCHAR(50),
            lastname VARCHAR(50),
            dob DATE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            user_type VARCHAR(50) NOT NULL DEFAULT 'resident',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Houses (
            house_id INT AUTO_INCREMENT PRIMARY KEY,
            
            house_name VARCHAR(100) NOT NULL,
            address VARCHAR(255) NOT NULL,
            owner_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT fk_house_owner 
                FOREIGN KEY (owner_id) REFERENCES Users(user_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Residents (
            resident_id INT AUTO_INCREMENT PRIMARY KEY,
            house_id INT NOT NULL,
            user_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT fk_resident_house 
                FOREIGN KEY (house_id) REFERENCES Houses(house_id) ON DELETE CASCADE,
            CONSTRAINT fk_resident_user 
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Calendar (
            calendar_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            calendar_name VARCHAR(100) NOT NULL,
            description VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT fk_calendar_user
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Calendar_Event (
            calendar_event_id INT AUTO_INCREMENT PRIMARY KEY,
            calendar_id INT NOT NULL,
            event_title VARCHAR(255) NOT NULL,
            event_description TEXT,
            start_datetime DATETIME NOT NULL,
            end_datetime DATETIME NOT NULL,
            access_level ENUM('private', 'shared', 'public') DEFAULT 'private',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT fk_calendar_event
                FOREIGN KEY (calendar_id) REFERENCES Calendar(calendar_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS User_Mail (
            user_mail_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            mail_access_level ENUM('private', 'public', 'restricted') DEFAULT 'private',
            subject VARCHAR(255) NOT NULL,
            message TEXT,
            mail_status ENUM('unread', 'read') DEFAULT 'unread',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT fk_user_mail_user
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Bill_Info (
            bill_id INT AUTO_INCREMENT PRIMARY KEY,
            bill_name VARCHAR(100) NOT NULL,
            bill_type VARCHAR(50) NOT NULL,
            total_consumption DECIMAL(10,2) NOT NULL DEFAULT 0.00,
            amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
            house_id INT NOT NULL,
            user_id INT NOT NULL,
            access_level ENUM('owner_only', 'shared', 'public') DEFAULT 'owner_only',
            due_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT fk_bill_house
                FOREIGN KEY (house_id) REFERENCES Houses(house_id) ON DELETE CASCADE,
            CONSTRAINT fk_bill_user
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Notification (
            notification_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            calendar_event_id INT NULL,
            bill_id INT NULL,
            notification_type ENUM('calendar_event', 'bill_info') NOT NULL,
            read_status ENUM('unread', 'read') DEFAULT 'unread',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT fk_notification_user
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
            CONSTRAINT fk_notification_event
                FOREIGN KEY (calendar_event_id) REFERENCES Calendar_Event(calendar_event_id) ON DELETE CASCADE,
            CONSTRAINT fk_notification_bill
                FOREIGN KEY (bill_id) REFERENCES Bill_Info(bill_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Sensors_Info (
            sensor_id INT AUTO_INCREMENT PRIMARY KEY,
            sensor_name VARCHAR(100) NOT NULL,
            sensor_type VARCHAR(50) NOT NULL,
            sensor_manufacturer VARCHAR(100) NOT NULL,
            house_id INT NOT NULL,
            sensor_unit VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT fk_sensors_house
                FOREIGN KEY (house_id) REFERENCES Houses(house_id) ON DELETE CASCADE
        );
        """
    ]

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            for ddl in TABLES:
                cursor.execute(ddl)
        conn.commit()
        print("All tables created or exist already.")
    finally:
        conn.close()

# SQLAlchemy setup
DATABASE_URL = (
    f"mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency function to get a new SQLAlchemy Session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
