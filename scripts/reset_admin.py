import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from werkzeug.security import generate_password_hash
from app.database import get_db_connection
import sqlite3

def reset_admin():
    email = 'admin@sparklewash.com'
    password = 'admin123'
    hashed_pw = generate_password_hash(password)
    
    conn = get_db_connection()
    
    # Check if admin exists
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    
    if user:
        print(f"Updating password for {email}...")
        conn.execute('UPDATE users SET password_hash = ? WHERE email = ?', (hashed_pw, email))
    else:
        print(f"Creating admin user {email}...")
        conn.execute('''
            INSERT INTO users (name, email, phone, password_hash, role, vehicle_no, vehicle_type) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('Admin User', email, '000-000-0000', hashed_pw, 'admin', 'ADMIN', 'None'))
        
    conn.commit()
    conn.close()
    print(f"Admin credentials set:\nEmail: {email}\nPassword: {password}")

if __name__ == '__main__':
    reset_admin()
