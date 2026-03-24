import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "weather_db"),
        user=os.getenv("DB_USER", "pipeline_user"),
        password=os.getenv("DB_PASSWORD", "pipeline_pass"),
    )

def load_weather_metrics(records: list):
    conn = get_connection()
    cursor = conn.cursor()

    for record in records:
        cursor.execute("""
            INSERT INTO raw.weather_metrics (
                city, country, collected_at, temp, temp_min, temp_max,
                humidity, pressure, weather, wind_speed, cloudiness
            ) VALUES (
                %(city)s, %(country)s, %(collected_at)s, %(temp)s, 
                %(temp_min)s, %(temp_max)s, %(humidity)s, %(pressure)s, 
                %(weather)s, %(wind_speed)s, %(cloudiness)s
                )
            """, record)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{len(records)} registros inseridos no banco.")

            