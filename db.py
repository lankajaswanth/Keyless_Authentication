import psycopg2
from dotenv import load_dotenv
load_dotenv()
import os


conn = None
def connect():
    global conn
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database =os.getenv('DB_NAME'),
    )
    conn.autocommit = True
    return True

def disconnect():
    global conn
    conn.close()
    return True

def create():
    cur = conn.cursor()
    q = '''CREATE TABLE IF NOT EXISTS tempusers(
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        token VARCHAR(255) NOT NULL,
        encodings TEXT NOT NULL
    )'''
    cur.execute(q)
    cur.close()
    return True

def select(query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows

def insert(query):
    cur = conn.cursor()
    cur.execute(query)
    cur.close()
    return True