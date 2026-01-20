import os
import sys

# Add the project root to the python path so 'app' module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

app = create_app()

# Vercel needs 'app' variable to be the WSGI application
