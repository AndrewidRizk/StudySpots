# backend/app/routes/simple_swagger.py

from flask import Blueprint, jsonify, render_template_string

swagger_bp = Blueprint('swagger', __name__)

# OpenAPI specification for your API
openapi_spec = {
    "openapi": "3.0.0",
    "info": {
        "title": "StudySpots API",
        "description": "A comprehensive API for finding and managing study spots at York University",
        "version": "1.0.0"
    },
    "servers": [
        {
            "url": "http://127.0.0.1:5001",
            "description": "Development server"
        }
    ],
    "paths": {
        "/api/study-spots": {
            "get": {
                "summary": "Get all study spots",
                "description": "Fetch all study spots including lecture halls, cafes, and libraries",
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Building"
                                    }
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Internal server error"
                    }
                }
            }
        },
        "/api/health": {
            "get": {
                "summary": "API health check",
                "description": "Comprehensive API health check for all services",
                "responses": {
                    "200": {
                        "description": "Health status",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HealthStatus"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/dashboard": {
            "get": {
                "summary": "Developer dashboard",
                "description": "Access the developer dashboard with API monitoring tools",
                "responses": {
                    "200": {
                        "description": "Dashboard HTML page"
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Building": {
                "type": "object",
                "properties": {
                    "building": {
                        "type": "string",
                        "description": "Building name",
                        "example": "Lassonde Building"
                    },
                    "building_code": {
                        "type": "string",
                        "description": "Building code",
                        "example": "LAS"
                    },
                    "building_status": {
                        "type": "string",
                        "description": "Overall building status",
                        "enum": ["Available", "Opening Soon", "Unavailable"]
                    },
                    "location": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "Coordinates [longitude, latitude]",
                        "example": [-79.503471, 43.772861]
                    },
                    "distance": {
                        "type": "number",
                        "description": "Distance from user location in km"
                    },
                    "type": {
                        "type": "string",
                        "description": "Type of study spot",
                        "enum": ["lecture_hall", "cafe", "library"]
                    },
                    "rooms": {
                        "type": "object",
                        "description": "Dictionary of rooms (for lecture halls)"
                    },
                    "slots": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/Slot"
                        },
                        "description": "Available time slots (for cafes and libraries)"
                    },
                    "website": {
                        "type": "string",
                        "description": "Website URL"
                    }
                }
            },
            "Slot": {
                "type": "object",
                "properties": {
                    "StartTime": {
                        "type": "string",
                        "description": "Start time in HH:MM format",
                        "example": "09:00"
                    },
                    "EndTime": {
                        "type": "string",
                        "description": "End time in HH:MM format",
                        "example": "10:30"
                    },
                    "Status": {
                        "type": "string",
                        "description": "Slot status",
                        "example": "Available"
                    }
                }
            },
            "HealthStatus": {
                "type": "object",
                "properties": {
                    "timestamp": {
                        "type": "string",
                        "description": "Timestamp of health check"
                    },
                    "status": {
                        "type": "string",
                        "description": "Overall API status",
                        "enum": ["healthy", "degraded", "unhealthy"]
                    },
                    "services": {
                        "type": "object",
                        "description": "Dictionary of service health statuses"
                    }
                }
            }
        }
    }
}

@swagger_bp.route('/api/swagger/')
@swagger_bp.route('/api/swagger')
def swagger_ui():
    """Serve Swagger UI"""
    swagger_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>StudySpots API Documentation</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
        <style>
            html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
            *, *:before, *:after { box-sizing: inherit; }
            body { margin:0; background: #fafafa; }
            .swagger-ui .topbar { background: linear-gradient(135deg, #007acc, #005a9e); border-bottom: 2px solid #004080; }
            .swagger-ui .topbar .download-url-wrapper { display: none; }
            .swagger-ui .info .title { color: #007acc; font-size: 2.5rem; font-weight: 300; }
            .swagger-ui .info .description { color: #666; font-size: 1.1rem; line-height: 1.6; }
            .swagger-ui .scheme-container { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; margin: 20px 0; }
            .swagger-ui .opblock.opblock-get { border-color: #28a745; background: rgba(40, 167, 69, 0.1); }
            .swagger-ui .opblock.opblock-get .opblock-summary { border-color: #28a745; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: '/api/openapi.json',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout"
                });
            };
        </script>
    </body>
    </html>
    '''
    return swagger_html

@swagger_bp.route('/api/openapi.json')
def openapi_json():
    """Serve OpenAPI specification as JSON"""
    return jsonify(openapi_spec)
