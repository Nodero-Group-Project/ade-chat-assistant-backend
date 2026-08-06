import psycopg2
from psycopg2.extras import RealDictCursor
import csv
from dotenv import load_dotenv
import os

load_dotenv()

CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

def executeQuery(query):
    print(CONNECTION_STRING)
    connection = None

    try:
        connection = psycopg2.connect(CONNECTION_STRING)

        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        return rows

    except Exception as e:
        print(f"Database error: {e}")
        return None

    finally:
        if connection:
            connection.close()

def write_csv(data, csv_file):

    if not data:
        return

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
