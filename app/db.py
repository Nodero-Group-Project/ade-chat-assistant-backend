import psycopg2
from psycopg2.extras import RealDictCursor
import csv

CONNECTION_STRING = "postgresql://neondb_owner:npg_E1DosxFB9wpY@ep-bitter-sky-axnzj54r.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require"

def executeQuery(query):

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