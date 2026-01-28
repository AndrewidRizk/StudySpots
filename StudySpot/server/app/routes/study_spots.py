# backend/app/routes/study_spots.py

from flask import Blueprint, jsonify
from app.database import get_lecture_halls, get_cafes, get_libraries, get_all_locations

study_spots_bp = Blueprint('study_spots', __name__)

@study_spots_bp.route('/study-spots/', methods=['GET'])
@study_spots_bp.route('/study-spots', methods=['GET'])
def fetch_study_spots():
    """
    Combines lecture halls, cafes, and libraries into a single JSON array.
    """
    try:
        # Fetch data from each function
        lecture_halls = get_lecture_halls()  # Fetch lecture halls
        cafes = get_cafes()  # Fetch cafes
        libraries = get_libraries()  # Fetch libraries

        # Add `type` attribute to distinguish between categories
        lecture_halls_with_type = [{"type": "lecture_hall", **hall} for hall in lecture_halls]
        cafes_with_type = [{"type": "cafe", **cafe} for cafe in cafes]
        libraries_with_type = [{"type": "library", **library} for library in libraries]

        # Combine all into a single list
        combined_data = lecture_halls_with_type + cafes_with_type + libraries_with_type

        return jsonify(combined_data), 200  # Return combined data with HTTP status 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return an error response if something goes wrong

@study_spots_bp.route('/locations/', methods=['GET'])
@study_spots_bp.route('/locations', methods=['GET'])
def fetch_locations():
    """
    Fetches all building locations for the dev form dropdown.
    """
    try:
        locations = get_all_locations()
        return jsonify(locations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
