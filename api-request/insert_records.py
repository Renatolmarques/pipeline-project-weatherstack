# -*- coding: utf-8 -*-
import psycopg2
from api_request import mock_fetch_data
# New packages for random data generation
import random
from datetime import datetime, timedelta

def connect_to_db():
    """
    Establishes a connection to the PostgreSQL database using credentials.
    """
    print("Connecting to the PostgreSQL database....")
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5001,
            dbname="db",
            user="db_user",
            password="db_password"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise

def create_table(conn):
    """
    Ensures the target schema and table exist in the database.
    Uses 'CREATE IF NOT EXISTS' to avoid errors on subsequent runs.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature FLOAT,
                weather_descriptions TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                -- ADD THIS LINE BACK
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT
            );
        """)
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise

def insert_data(conn, weather_data):
    """
    Extracts relevant fields from the weather_data JSON object
    and inserts them into the dev.raw_weather_data table.
    """
    try:
        cursor = conn.cursor()
        
        # Extracting data from the JSON object to match our table columns
        city = weather_data['location']['name']
        temperature = weather_data['current']['temperature']
        weather_descriptions = ', '.join(weather_data['current']['weather_descriptions'])
        wind_speed = weather_data['current']['wind_speed']
        observation_time = weather_data['location']['localtime'] 
        utc_offset = weather_data['location']['utc_offset']
        
        # SQL query to insert data, using placeholders (%s) for security
        insert_query = """
            INSERT INTO dev.raw_weather_data 
            (city, temperature, weather_descriptions, wind_speed, time, utc_offset) 
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        
        # A tuple containing the values to be inserted
        record_to_insert = (city, temperature, weather_descriptions, wind_speed, observation_time, utc_offset)
        cursor.execute(insert_query, record_to_insert)
        conn.commit()
        
    except psycopg2.Error as e:
        print(f"Failed to insert data: {e}")
        conn.rollback() # Roll back the transaction in case of an error
        raise
    finally:
        # Ensure the cursor is closed
        if cursor:
            cursor.close()

# --- MAIN EXECUTION BLOCK ---
if __name__ == '__main__':
    conn = None # Initialize connection to null
    try:
        conn = connect_to_db()
        create_table(conn)
        print("Table checked/created.")
        
        cities = ["Recife", "Olinda", "Caruaru", "Petrolina", "Jaboatão dos Guararapes", 
                  "Paulista", "Garanhuns", "Vitória de Santo Antão", "Ipojuca", "Serra Talhada"]
        
        print(f"Starting to insert 1000 records...")
        
        # Loop to insert 1000 records
        for i in range(1000):
            # Get the mock data template
            weather_data = mock_fetch_data()
            
            # Modify the data to create variety
            weather_data['location']['name'] = random.choice(cities)
            weather_data['current']['temperature'] += random.uniform(-5.0, 5.0)
            weather_data['current']['wind_speed'] += random.uniform(-5.0, 5.0)
            
            # Convert string date to datetime object, subtract random days, and convert back to string
            original_time = datetime.strptime(weather_data['location']['localtime'], '%Y-%m-%d %H:%M')
            new_time = original_time - timedelta(days=random.randint(0, 365))
            weather_data['location']['localtime'] = new_time.strftime('%Y-%m-%d %H:%M')
            
            # Insert the modified record
            insert_data(conn, weather_data)
            
            if (i + 1) % 100 == 0:
                print(f"{i + 1}/1000 records inserted...")

        print("Finished inserting all records.")
        
    except Exception as e:
        print(f"An error occurred in the main execution block: {e}")
        
    finally:
        # Close the database connection
        if conn:
            conn.close()
            print("Database connection closed.")