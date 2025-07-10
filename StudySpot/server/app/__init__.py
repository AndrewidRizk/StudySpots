# backend/app/__init__.py

from flask import Flask
from flask_cors import CORS  # Import Flask-Cors
from app.config import Config
from app.routes.test_connection import test_bp
from app.routes.study_spots import study_spots_bp
import pytz
from datetime import datetime

def create_app():
    """
    Function responsible for registering the routs and accespting the requests
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    TORONTO_TZ = pytz.timezone('America/Toronto')  # Replace with your timezone

    def get_toronto_time():
        """Helper function to get the current time in Toronto timezone."""
        return datetime.now(TORONTO_TZ)
    
    print(f"App initialized at {get_toronto_time()} Toronto time.")

    
    # Enable CORS for the app
    # Allow only requests from the frontend at http://localhost:3000
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(test_bp, url_prefix="/api")
    app.register_blueprint(study_spots_bp, url_prefix="/api")

    return app
