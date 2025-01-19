# studyspot/database.py

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import timedelta  # Import timedelta
from app.config import Config  # Import Config for environment variables
from datetime import datetime
from datetime import timedelta
import pytz

# Load environment variables from .env
load_dotenv()
toronto_tz = pytz.timezone('America/Toronto')
current_time = datetime.now(toronto_tz)

def create_connection():
    """Establishes and returns a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(connection):
    """Closes the database connection."""
    if connection and connection.is_connected():
        connection.close()


def get_lecture_halls():
    """
    Fetches all records for the current day and formats the output.
    """
    from datetime import datetime

    print("Starting get_lecture_halls function...")  # Debugging log
    
    connection = create_connection()
    if connection is None:
        return []
    

    try:
        cursor = connection.cursor(dictionary=True)

        # Get the current day of the week
        day_map = ["M", "T", "W", "R", "F", "S", "U"]
        current_day = day_map[datetime.now().weekday()]
        current_time = datetime.now(toronto_tz)
        print(f"The current time in Toronto is {current_time.strftime('%Y-%m-%d %H:%M:%S')} and the day is {current_day}.")

        # Query the database
        query = """
        SELECT 
            b.building_name AS building,
            b.building_code AS building_code,
            ST_AsText(b.location) AS location,
            r.room_name AS roomNumber,
            a.start_time AS StartTime,
            a.end_time AS EndTime,
            CASE 
                WHEN TIME(NOW()) BETWEEN a.start_time AND a.end_time THEN 'Upcoming'
                ELSE 'Available'
            END AS Status
        FROM buildings b
        JOIN rooms r ON b.building_id = r.building_id
        JOIN availabilities a ON r.room_id = a.room_id
        WHERE a.day = %s
        ORDER BY b.building_name, r.room_name, a.start_time;
        """
    
        cursor.execute(query, (current_day,))
        result = cursor.fetchall()

        # Format the data
        if not result:
            
            return []

        def parse_location(location):
            if location and location.startswith("POINT("):
                coords = location[6:-1].split()
                return tuple(map(float, coords))
            return None
        
        def format_time(value):
            if isinstance(value, timedelta):
                # Convert timedelta to hours and minutes
                total_seconds = value.total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                return f"{hours:02}:{minutes:02}"
            elif isinstance(value, datetime):
                # If it's already a datetime object, format directly
                return value.strftime("%H:%M")
            return value  # For other cases, return as-is

        buildings = {}
        for row in result:
            building_name = row["building"]
            building_code = row["building_code"]
            location = parse_location(row["location"])
            room_number = row["roomNumber"]
            start_time = format_time(row["StartTime"])
            end_time = format_time(row["EndTime"])
            status = ""

            if building_name not in buildings:
                buildings[building_name] = {
                    "building": building_name,
                    "building_code": building_code,
                    "location": location,
                    "building_status": "",
                    "rooms": {},
                }

            if room_number not in buildings[building_name]["rooms"]:
                buildings[building_name]["rooms"][room_number] = {
                    "roomNumber": room_number,
                    "slots": []
                }

            buildings[building_name]["rooms"][room_number]["slots"].append({
                "StartTime": start_time,
                "EndTime": end_time,
                "Status": status
            })

        
        return list(buildings.values())
    except Exception as e:
        print(f"Error fetching study spots: {e}")
        return []
    finally:
        close_connection(connection)
        print("Lec Halls, Database connection closed.")  # Debugging log

def get_cafes():
    """
    Fetches all cafes and their availability for the current day.
    """
    from datetime import datetime

    print("Starting get_cafes function...")  # Debugging log

    connection = create_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        # Get the current day of the week
        day_map = ["M", "T", "W", "R", "F", "S", "U"]
        current_day = day_map[datetime.now().weekday()]

        # Query the database
        query = """
        SELECT 
            c.name AS cafe_name,
            ST_AsText(c.location) AS location,
            a.open_time AS StartTime,
            a.close_time AS EndTime
        FROM cafes c
        JOIN facility_availabilities a ON c.cafe_id = a.facility_id
        WHERE a.facility_type = 'cafe' AND a.day = %s
        ORDER BY c.name, a.open_time;
        """

        cursor.execute(query, (current_day,))
        result = cursor.fetchall()

        # Format the data
        if not result:
            return []
        
        def parse_location(location):
            if location and location.startswith("POINT("):
                coords = location[6:-1].split()
                return tuple(map(float, coords))
            return None
        def format_time(value):
            if isinstance(value, timedelta):
                # Convert timedelta to hours and minutes
                total_seconds = value.total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                return f"{hours:02}:{minutes:02}"
            elif isinstance(value, datetime):
                # If it's already a datetime object, format directly
                return value.strftime("%H:%M")
            return value  # For other cases, return as-is

        cafes = {}
        for row in result:
            cafe_name = row["cafe_name"]
            location = parse_location(row["location"])
            start_time = format_time(row["StartTime"])
            end_time = format_time(row["EndTime"])

            if cafe_name not in cafes:
                cafes[cafe_name] = {
                    "building": cafe_name,
                    "location": location,
                    "building_code": "",
                    "building_status": "",
                    "rooms": {},
                    "slots": [],  # Initialize slots properly
                }

            cafes[cafe_name]["slots"].append({
                "StartTime": start_time,
                "EndTime": end_time,
                "Status": []
            })

        return list(cafes.values())
    except Exception as e:
        print(f"Error fetching cafes: {e}")
        return []
    finally:
        close_connection(connection)
        print("Database connection closed.")  # Debugging log

def get_libraries():
    """
    Fetches all libraries and their availability for the current day.
    """
    from datetime import datetime

    print("Starting get_libraries function...")  # Debugging log

    connection = create_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        # Get the current day of the week
        day_map = ["M", "T", "W", "R", "F", "S", "U"]
        current_day = day_map[datetime.now().weekday()]

        # Query the database
        query = """
        SELECT 
            l.name AS library_name,
            ST_AsText(l.location) AS location,
            l.website AS website,
            a.open_time AS StartTime,
            a.close_time AS EndTime
        FROM libraries l
        JOIN facility_availabilities a ON l.library_id = a.facility_id
        WHERE a.facility_type = 'library' AND a.day = %s
        ORDER BY l.name, a.open_time;
        """

        cursor.execute(query, (current_day,))
        result = cursor.fetchall()

        # Format the data
        if not result:
            return []

        def parse_location(location):
            if location and location.startswith("POINT("):
                coords = location[6:-1].split()
                return tuple(map(float, coords))
            return None
        
        def format_time(value):
            if isinstance(value, timedelta):
                # Convert timedelta to hours and minutes
                total_seconds = value.total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                return f"{hours:02}:{minutes:02}"
            elif isinstance(value, datetime):
                # If it's already a datetime object, format directly
                return value.strftime("%H:%M")
            return value  # For other cases, return as-is

        libraries = {}
        for row in result:
            library_name = row["library_name"]
            location = parse_location(row["location"])
            website = row["website"]
            start_time = format_time(row["StartTime"])
            end_time = format_time(row["EndTime"])

            if library_name not in libraries:
                libraries[library_name] = {
                    "building": library_name,
                    "location": location,
                    "building_code": "",
                    "website": website,
                    "building_status": "",
                    "rooms": {},
                    "slots": []
                }

            libraries[library_name]["slots"].append({
                "StartTime": start_time,
                "EndTime": end_time,
                "Status": ""
            })

        return list(libraries.values())
    except Exception as e:
        print(f"Error fetching libraries: {e}")
        return []
    finally:
        close_connection(connection)
        print("Database connection closed.")  # Debugging log