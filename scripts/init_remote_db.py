import os
import sys

# Ensure we can import from the app package (parent directory)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import init_db

if __name__ == '__main__':
    print("Initializing database...")
    try:
        init_db()
        print("Database initialization complete!")
    except Exception as e:
        print(f"Error initializing database: {e}")
