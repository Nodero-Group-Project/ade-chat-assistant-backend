import psycopg
from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")

@dataclass
class Intent:
    Description: str

@dataclass
class Dataset:
    Id: str
    Name: str
    Description: str
    Skill: str


def intent_get_all() -> list[Intent]:
    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM intent order by Description asc')

            return [
                Intent(Description=row[0])
                for row in cursor.fetchall()
            ]

def intent_insert(description: str) -> None:
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

def intent_delete(description: str) -> bool:
    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'DELETE FROM intent WHERE LOWER(Description) = LOWER(%s)',
                (description,)
            )

            return cursor.rowcount > 0


def dataset_get_all() -> list[Dataset]:
    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM dataset order by Id asc'
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

def dataset_insert(id:str,name:str,description:str,skill:str) -> None:
    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO dataset (Id, Name, Description, Skill) VALUES (%s, %s, %s, %s)',
                (
                    id,name,description,skill
                )
            )

def dataset_exists(id: str) -> bool:
    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT EXISTS('
                'SELECT 1 FROM dataset WHERE Id = %s'
                ')',
                (id,)
            )

            return cursor.fetchone()[0]

def dataset_delete(id: str) -> bool:
    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'DELETE FROM dataset WHERE LOWER(ID) = LOWER(%s)',
                (id,)
            )

            return cursor.rowcount > 0

def dataset_update(id:str,name:str,description:str,skill:str) -> bool:
    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'UPDATE dataset '
                'SET Name = %s, '
                'Description = %s, '
                'Skill = %s '
                'WHERE Id = %s',
                (
                    name,
                    description,
                    skill,
                    id
                )
            )

            return cursor.rowcount > 0