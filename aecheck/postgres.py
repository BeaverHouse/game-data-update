import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_postgres():
    return psycopg2.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DBNAME"),
    )