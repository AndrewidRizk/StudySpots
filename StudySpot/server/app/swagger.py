# backend/app/swagger.py

from flask_restx import Api, Resource, fields
from flask import Blueprint
from werkzeug.security import check_password_hash, generate_password_hash

# Create API blueprint
api_bp = Blueprint('api', __name__)

# Initialize Flask-RESTX API
api = Api(
    api_bp,
    version='1.0',
    title='StudySpots API',
    description='A comprehensive API for finding and managing study spots at York University',
    doc='/swagger/',
    prefix='/api'
)

# Custom CSS for Swagger UI
custom_css = """
<style>
    .swagger-ui .topbar { 
        background: linear-gradient(135deg, #007acc, #005a9e);
        border-bottom: 2px solid #004080;
    }
    .swagger-ui .topbar .download-url-wrapper { 
        display: none; 
    }
    .swagger-ui .info .title {
        color: #007acc;
        font-size: 2.5rem;
        font-weight: 300;
    }
    .swagger-ui .info .description {
        color: #666;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .swagger-ui .scheme-container {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin: 20px 0;
    }
    .swagger-ui .opblock.opblock-get {
        border-color: #28a745;
        background: rgba(40, 167, 69, 0.1);
    }
    .swagger-ui .opblock.opblock-get .opblock-summary {
        border-color: #28a745;
    }
    .swagger-ui .opblock.opblock-post {
        border-color: #007bff;
        background: rgba(0, 123, 255, 0.1);
    }
    .swagger-ui .btn.authorize {
        background: linear-gradient(135deg, #007acc, #005a9e);
        border-color: #007acc;
    }
    .swagger-ui .btn.authorize:hover {
        background: linear-gradient(135deg, #1e88e5, #1565c0);
    }
</style>
"""

# Add custom CSS to Swagger UI
@api.documentation
def custom_ui():
    return custom_css

# Data models for Swagger documentation
slot_model = api.model('Slot', {
    'StartTime': fields.String(required=True, description='Start time in HH:MM format', example='09:00'),
    'EndTime': fields.String(required=True, description='End time in HH:MM format', example='10:30'),
    'Status': fields.String(required=True, description='Slot status', example='Available')
})

room_model = api.model('Room', {
    'roomNumber': fields.String(required=True, description='Room number', example='101'),
    'slots': fields.List(fields.Nested(slot_model), description='Available time slots')
})

building_model = api.model('Building', {
    'building': fields.String(required=True, description='Building name', example='Lassonde Building'),
    'building_code': fields.String(required=True, description='Building code', example='LAS'),
    'building_status': fields.String(required=True, description='Overall building status', example='Available'),
    'location': fields.List(fields.Float, description='Coordinates [longitude, latitude]', example=[-79.503471, 43.772861]),
    'distance': fields.Float(description='Distance from user location in km', example=0.5),
    'type': fields.String(required=True, description='Type of study spot', enum=['lecture_hall', 'cafe', 'library']),
    'rooms': fields.Raw(description='Dictionary of rooms (for lecture halls)'),
    'slots': fields.List(fields.Nested(slot_model), description='Available time slots (for cafes and libraries)'),
    'website': fields.String(description='Website URL', example='https://example.com')
})

health_service_model = api.model('HealthService', {
    'status': fields.String(required=True, description='Service status', enum=['healthy', 'unhealthy']),
    'response_time_ms': fields.Float(description='Response time in milliseconds'),
    'count': fields.Integer(description='Number of items returned'),
    'total_count': fields.Integer(description='Total number of items'),
    'error': fields.String(description='Error message if unhealthy')
})

health_status_model = api.model('HealthStatus', {
    'timestamp': fields.String(required=True, description='Timestamp of health check'),
    'status': fields.String(required=True, description='Overall API status', enum=['healthy', 'degraded', 'unhealthy']),
    'services': fields.Raw(description='Dictionary of service health statuses')
})

# Basic authentication check
def authenticate():
    """Simple authentication for Swagger UI access"""
    # You can customize these credentials
    valid_username = "admin"
    valid_password = "admin"
    
    from flask import request
    import base64
    
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return False
    
    return auth.username == valid_username and auth.password == valid_password

def require_auth(f):
    """Decorator to require authentication"""
    from functools import wraps
    from flask import request, Response
    
    @wraps(f)
    def decorated(*args, **kwargs):
        if not authenticate():
            return Response(
                'Authentication required.\n'
                'Default credentials: admin/admin', 401,
                {'WWW-Authenticate': 'Basic realm="StudySpots API"'})
        return f(*args, **kwargs)
    return decorated

# Note: Authentication can be added later if needed
