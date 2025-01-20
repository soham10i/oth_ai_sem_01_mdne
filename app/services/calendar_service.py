from app.database.connection import get_connection
from fastapi import HTTPException

class CalendarService:
    def __init__(self):
        """
        Initialize the CalendarService with MySQL connection.
        """
        try:
            self.mysql_conn = get_connection()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error initializing CalendarService: {str(e)}")

    def create_calendar(self, user_id, calendar_name, description):
        """
        Create a new calendar in the database.
        
        :param user_id: ID of the user creating the calendar
        :param calendar_name: Name of the calendar
        :param description: Description of the calendar
        :return: ID of the created calendar
        """
        query = """
        INSERT INTO Calendar (user_id, calendar_name, description) 
        VALUES (%s, %s, %s)
        """
        try:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(query, (user_id, calendar_name, description))
                self.mysql_conn.commit()
                return cursor.lastrowid
        except Exception as e:
            self.mysql_conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating calendar: {str(e)}")

    def get_calendars(self, user_id):
        """
        Retrieve all calendars for a specific user.
        
        :param user_id: ID of the user
        :return: List of calendars for the user
        """
        query = "SELECT * FROM Calendar WHERE user_id = %s"
        try:
            with self.mysql_conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving calendars: {str(e)}")

    def delete_calendar(self, calendar_id):
        """
        Delete a calendar from the database.
        
        :param calendar_id: ID of the calendar to delete
        """
        query = "DELETE FROM Calendar WHERE calendar_id = %s"
        try:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(query, (calendar_id,))
                self.mysql_conn.commit()
        except Exception as e:
            self.mysql_conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting calendar: {str(e)}")

    def create_event(self, calendar_id, event_title, start_datetime, end_datetime, is_recurring, recurrence_rule, recurrence_end_date, access_level, event_description):
        """
        Create a new event in the calendar.
        
        :param calendar_id: ID of the calendar
        :param event_title: Title of the event
        :param start_datetime: Start datetime of the event
        :param end_datetime: End datetime of the event
        :param is_recurring: Boolean indicating if the event is recurring
        :param recurrence_rule: Recurrence rule for the event
        :param recurrence_end_date: End date for the recurrence
        :param access_level: Access level for the event
        :param event_description: Description of the event
        :return: ID of the created event
        """
        query = """
        INSERT INTO Calendar_Event (calendar_id, event_title, start_datetime, end_datetime, 
        is_recurring, recurrence_rule, recurrence_end_date, access_level, event_description) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(query, (calendar_id, event_title, start_datetime, end_datetime, is_recurring, recurrence_rule, recurrence_end_date, access_level, event_description))
                self.mysql_conn.commit()
                return cursor.lastrowid
        except Exception as e:
            self.mysql_conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating event: {str(e)}")

    def get_events(self, calendar_id, start_datetime=None, end_datetime=None):
        """
        Retrieve all events for a specific calendar, optionally filtered by date range.
        
        :param calendar_id: ID of the calendar
        :param start_datetime: Optional start datetime to filter events
        :param end_datetime: Optional end datetime to filter events
        :return: List of events for the calendar
        """
        query = "SELECT * FROM Calendar_Event WHERE calendar_id = %s"
        params = [calendar_id]
        if start_datetime and end_datetime:
            query += " AND start_datetime >= %s AND end_datetime <= %s"
            params.extend([start_datetime, end_datetime])
        try:
            with self.mysql_conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, tuple(params))
                return cursor.fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving events: {str(e)}")

    def delete_event(self, event_id):
        """
        Delete an event from the calendar.
        
        :param event_id: ID of the event to delete
        """
        query = "DELETE FROM Calendar_Event WHERE calendar_event_id = %s"
        try:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(query, (event_id,))
                self.mysql_conn.commit()
        except Exception as e:
            self.mysql_conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting event: {str(e)}")

    def share_event(self, event_id, shared_with_user_id, share_access_level):
        """
        Share an event with another user.
        
        :param event_id: ID of the event to share
        :param shared_with_user_id: ID of the user to share the event with
        :param share_access_level: Access level for the shared event
        """
        query = """
        INSERT INTO Calendar_Event_Share (calendar_event_id, shared_with_user_id, share_access_level) 
        VALUES (%s, %s, %s)
        """
        try:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(query, (event_id, shared_with_user_id, share_access_level))
                self.mysql_conn.commit()
        except Exception as e:
            self.mysql_conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error sharing event: {str(e)}")

    def get_shared_events(self, user_id):
        """
        Retrieve all events shared with a specific user.
        
        :param user_id: ID of the user
        :return: List of shared events for the user
        """
        query = """
        SELECT ce.* FROM Calendar_Event_Share ces
        JOIN Calendar_Event ce ON ces.calendar_event_id = ce.calendar_event_id
        WHERE ces.shared_with_user_id = %s
        """
        try:
            with self.mysql_conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving shared events: {str(e)}")

    def update_share_access(self, event_share_id, share_access_level):
        """
        Update the access level for a shared event.
        
        :param event_share_id: ID of the shared event
        :param share_access_level: New access level for the shared event
        """
        query = "UPDATE Calendar_Event_Share SET share_access_level = %s WHERE event_share_id = %s"
        try:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(query, (share_access_level, event_share_id))
                self.mysql_conn.commit()
        except Exception as e:
            self.mysql_conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating share access: {str(e)}")
