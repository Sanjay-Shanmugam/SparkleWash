import sqlite3
import os
from flask import g

DB_NAME = 'carwash.db'

def get_db_connection():
    # If running from root, DB is in root
    db_path = os.path.join(os.getcwd(), DB_NAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

    if db is not None:
        db.close()

def init_db():
    conn = get_db_connection()
    # Schema is in the same folder as this file (app/)
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        try:
            conn.executescript(f.read())
            print("Database initialized successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    conn.close()

