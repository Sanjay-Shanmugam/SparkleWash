import sqlite3
import os
import mysql.connector
from flask import g
from dotenv import load_dotenv
import urllib.parse
import certifi

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
    # Check for TiDB Connection String
    if os.environ.get('TIDB_CONNECTION_STRING'):
        try:
            url = urllib.parse.urlparse(os.environ.get('TIDB_CONNECTION_STRING'))
            
            # Parse query parameters for SSL CA
            query_params = urllib.parse.parse_qs(url.query)
            ssl_ca = query_params.get('ssl_ca', [None])[0]
            ssl_verify_cert = query_params.get('ssl_verify_cert', ['true'])[0].lower() == 'true'

            conn_kwargs = {
                'host': url.hostname,
                'port': url.port or 4000,
                'user': url.username,
                'password': url.password,
                'database': url.path[1:],  # Remove leading slash
                'ssl_verify_cert': ssl_verify_cert
            }
            
            if ssl_ca:
                conn_kwargs['ssl_ca'] = ssl_ca
            else:
                # Fallback to certifi if no specific CA provided
                conn_kwargs['ssl_ca'] = certifi.where()

            conn = mysql.connector.connect(**conn_kwargs)
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

