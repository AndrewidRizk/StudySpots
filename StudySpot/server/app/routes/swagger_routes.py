# backend/app/routes/swagger_routes.py

from flask_restx import Resource
from app.swagger import api, building_model, health_status_model
from app.database import get_lecture_halls, get_cafes, get_libraries
import time
from datetime import datetime

# Create namespace for study spots
ns_study_spots = api.namespace('study-spots', description='Study spots operations')
ns_health = api.namespace('health', description='API health monitoring')

@ns_study_spots.route('/')
class StudySpotsList(Resource):
    @api.doc('get_study_spots')
    @api.marshal_list_with(building_model)
    def get(self):
        """Fetch all study spots including lecture halls, cafes, and libraries"""
        try:
            # Fetch data from each function
            lecture_halls = get_lecture_halls()
            cafes = get_cafes()
            libraries = get_libraries()

            # Add `type` attribute to distinguish between categories
            lecture_halls_with_type = [{"type": "lecture_hall", **hall} for hall in lecture_halls]
            cafes_with_type = [{"type": "cafe", **cafe} for cafe in cafes]
            libraries_with_type = [{"type": "library", **library} for library in libraries]

            # Combine all into a single list
            combined_data = lecture_halls_with_type + cafes_with_type + libraries_with_type

            return combined_data, 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@ns_health.route('/')
class HealthCheck(Resource):
    @api.doc('api_health_check')
    @api.marshal_with(health_status_model)
    def get(self):
        """Comprehensive API health check for all services"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'services': {}
        }
        
        try:
            # Test lecture halls endpoint
            start_time = time.time()
            lecture_halls = get_lecture_halls()
            health_status['services']['lecture_halls'] = {
                'status': 'healthy',
                'response_time_ms': round((time.time() - start_time) * 1000, 2),
                'count': len(lecture_halls)
            }
        except Exception as e:
            health_status['services']['lecture_halls'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_status['status'] = 'degraded'
        
        try:
            # Test cafes endpoint
            start_time = time.time()
            cafes = get_cafes()
            health_status['services']['cafes'] = {
                'status': 'healthy',
                'response_time_ms': round((time.time() - start_time) * 1000, 2),
                'count': len(cafes)
            }
        except Exception as e:
            health_status['services']['cafes'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_status['status'] = 'degraded'
        
        try:
            # Test libraries endpoint
            start_time = time.time()
            libraries = get_libraries()
            health_status['services']['libraries'] = {
                'status': 'healthy',
                'response_time_ms': round((time.time() - start_time) * 1000, 2),
                'count': len(libraries)
            }
        except Exception as e:
            health_status['services']['libraries'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_status['status'] = 'degraded'
        
        # Test combined study-spots endpoint
        try:
            start_time = time.time()
            lecture_halls = get_lecture_halls()
            cafes = get_cafes()
            libraries = get_libraries()
            
            lecture_halls_with_type = [{"type": "lecture_hall", **hall} for hall in lecture_halls]
            cafes_with_type = [{"type": "cafe", **cafe} for cafe in cafes]
            libraries_with_type = [{"type": "library", **library} for library in libraries]
            
            combined_data = lecture_halls_with_type + cafes_with_type + libraries_with_type
            
            health_status['services']['study_spots'] = {
                'status': 'healthy',
                'response_time_ms': round((time.time() - start_time) * 1000, 2),
                'total_count': len(combined_data)
            }
        except Exception as e:
            health_status['services']['study_spots'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_status['status'] = 'degraded'
        
        return health_status, 200
