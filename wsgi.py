"""
WSGI entry point for Render deployment.
This file is used by Gunicorn to start the Flask application.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the Flask app
from app import app

if __name__ == '__main__':
    app.run()
