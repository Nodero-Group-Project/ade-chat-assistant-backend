import psycopg
from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")

# CONN_STR = "postgresql://neondb_owner:npg_HUNbyBRYx05K@ep-bitter-sky-axnzj54r.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require"


@dataclass
class Intent:
    Description: str


@dataclass
class Dataset:
    Id: str
    Name: str
    Description: str
    Skill: str


def get_all_intents() -> list[Intent]:
    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM intent order by Description asc')

            return [
                Intent(Description=row[0])
                for row in cursor.fetchall()
            ]


def get_all_datasets() -> list[Dataset]:
    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM dataset'
            )

            return [
                Dataset(
                    Id=row[0],
                    Name=row[1],
                    Description=row[2],
                    Skill=row[3]
                )
                for row in cursor.fetchall()
            ]

def add_intent(description: str) -> None:
    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO intent (Description) VALUES (%s)',
                (description,)
            )

def intent_exists(description: str) -> bool:
    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT EXISTS('
                'SELECT 1 FROM intent WHERE LOWER(Description) = LOWER(%s)'
                ')',
                (description,)
            )

            return cursor.fetchone()[0]

def delete_intent(description: str) -> bool:
    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'DELETE FROM intent WHERE LOWER(Description) = LOWER(%s)',
                (description,)
            )

            return cursor.rowcount > 0