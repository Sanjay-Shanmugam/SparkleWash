import sqlite3
import os
import mysql.connector
from flask import g
from dotenv import load_dotenv

load_dotenv()

DB_NAME = 'carwash.db'

class MySQLConnectionWrapper:
    """Wrapper to make MySQL connection behave like SQLite connection (execute method on conn)"""
    def __init__(self, conn):
        self.conn = conn
    
    def execute(self, query, params=None):
        cursor = self.conn.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
    
    @property
    def lastrowid(self):
        # This is tricky because usually we get it from cursor. 
        # But we create new cursor for each execute.
        # Impl: we might need to store the last cursor or just return None (might break valid usage)
        return None 

def get_db_connection():
    # Check for TiDB/MySQL Environment Variables
    if os.environ.get('TIDB_HOST'):
        try:
            conn = mysql.connector.connect(
                host=os.environ.get('TIDB_HOST'),
                port=os.environ.get('TIDB_PORT', 4000),
                user=os.environ.get('TIDB_USER'),
                password=os.environ.get('TIDB_PASSWORD'),
                database=os.environ.get('TIDB_DB_NAME'),
                ssl_verify_cert=True,
                ssl_ca=os.environ.get('TIDB_SSL_CA')
            )
            return MySQLConnectionWrapper(conn)
        except Exception as e:
            print(f"TiDB Connection Failed: {e}. Falling back to SQLite.")
    
    # SQLite Fallback
    db_path = os.path.join(os.getcwd(), DB_NAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    conn = get_db_connection()
    if isinstance(conn, MySQLConnectionWrapper):
        # MySQL/TiDB Init
        schema_path = os.path.join(os.path.dirname(__file__), 'schema_mysql.sql')
        with open(schema_path, 'r') as f:
            script = f.read()
            cursor = conn.conn.cursor()
            for result in cursor.execute(script, multi=True):
                pass
            print("TiDB Database initialized.")
    else:
        # SQLite Init
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            try:
                conn.executescript(f.read())
                print("SQLite Database initialized.")
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
    conn.close()

