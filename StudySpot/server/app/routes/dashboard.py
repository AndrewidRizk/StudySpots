# backend/app/routes/dashboard.py

from flask import Blueprint, jsonify
from app.database import get_lecture_halls, get_cafes, get_libraries
import requests
import time
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def developer_dashboard():
    """
    Developer dashboard with API health checks and navigation tools
    """
    # Return HTML directly to avoid template issues
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>StudySpots Developer Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1e1e1e; color: #cccccc; line-height: 1.6; min-height: 100vh; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #007acc, #005a9e); padding: 20px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0, 122, 204, 0.3); }
            .header h1 { color: white; font-size: 2.5rem; font-weight: 300; margin-bottom: 10px; }
            .header p { color: #e3f2fd; font-size: 1.1rem; }
            .dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .card { background-color: #252526; border: 1px solid #3c3c3c; border-radius: 8px; padding: 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3); transition: all 0.3s ease; }
            .card:hover { border-color: #007acc; box-shadow: 0 4px 16px rgba(0, 122, 204, 0.2); }
            .card h3 { color: #569cd6; font-size: 1.3rem; margin-bottom: 15px; }
            .btn { background: linear-gradient(135deg, #007acc, #005a9e); color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 1rem; font-weight: 500; text-decoration: none; display: inline-block; margin: 5px 5px 5px 0; transition: all 0.3s ease; }
            .btn:hover { background: linear-gradient(135deg, #1e88e5, #1565c0); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 122, 204, 0.4); }
            .btn-secondary { background: linear-gradient(135deg, #6c757d, #5a6268); }
            .health-status { margin-top: 15px; }
            .status-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; margin: 5px 0; background-color: #2d2d30; border-radius: 4px; border-left: 4px solid #6c757d; }
            .status-healthy { border-left-color: #28a745; }
            .status-unhealthy { border-left-color: #dc3545; }
            .status-degraded { border-left-color: #ffc107; }
            .status-badge { padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }
            .badge-healthy { background-color: #28a745; color: white; }
            .badge-unhealthy { background-color: #dc3545; color: white; }
            .badge-degraded { background-color: #ffc107; color: #212529; }
            .loading { display: inline-block; width: 20px; height: 20px; border: 3px solid #f3f3f3; border-top: 3px solid #007acc; border-radius: 50%; animation: spin 1s linear infinite; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .api-endpoints { background-color: #252526; border: 1px solid #3c3c3c; border-radius: 8px; padding: 20px; margin-top: 20px; }
            .endpoint { display: flex; align-items: center; gap: 10px; padding: 8px 12px; margin: 5px 0; background-color: #2d2d30; border-radius: 4px; font-family: 'Courier New', monospace; }
            .method { padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; }
            .method-get { background-color: #28a745; color: white; }
            .refresh-btn { float: right; background: transparent; border: 1px solid #569cd6; color: #569cd6; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 0.9rem; }
            .refresh-btn:hover { background-color: #569cd6; color: white; }
            .timestamp { font-size: 0.9rem; color: #888; margin-top: 10px; }
            .tools-section { background-color: #252526; border: 1px solid #3c3c3c; border-radius: 8px; padding: 20px; margin-bottom: 30px; }
            .tools-header h3 { color: #569cd6; font-size: 1.3rem; margin-bottom: 20px; }
            .tools-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .tool-item { background-color: #2d2d30; border-radius: 6px; padding: 15px; border-left: 4px solid #007acc; }
            .tool-item h4 { color: #cccccc; font-size: 1.1rem; margin-bottom: 10px; }
            .tool-buttons { display: flex; gap: 10px; flex-wrap: wrap; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>StudySpots Developer Dashboard</h1>
                <p>Monitor API health, access documentation, and manage your development environment</p>
            </div>
            <div class="tools-section">
                <div class="tools-header">
                    <h3>Developer Tools</h3>
                </div>
                <div class="tools-grid">
                    <div class="tool-item">
                        <h4>API Documentation</h4>
                        <div class="tool-buttons">
                            <a href="/api/swagger/" class="btn" target="_blank">Open Swagger UI</a>
                            <a href="/api/study-spots" class="btn btn-secondary" target="_blank">Test API</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="dashboard-grid">
                <div class="card">
                    <h3>API Health Monitor <button class="refresh-btn" onclick="checkHealth()">Refresh</button></h3>
                    <div id="health-status" class="health-status">
                        <div class="loading"></div> Checking API health...
                    </div>
                    <div id="last-updated" class="timestamp"></div>
                </div>
            </div>
            <div class="api-endpoints">
                <h3 style="color: #569cd6; margin-bottom: 15px;">Available API Endpoints</h3>
                <div class="endpoint">
                    <span class="method method-get">GET</span>
                    <span>/api/study-spots</span>
                    <span style="margin-left: auto; color: #888;">Get all study spots</span>
                </div>
                <div class="endpoint">
                    <span class="method method-get">GET</span>
                    <span>/api/health</span>
                    <span style="margin-left: auto; color: #888;">API health check</span>
                </div>
                <div class="endpoint">
                    <span class="method method-get">GET</span>
                    <span>/dashboard</span>
                    <span style="margin-left: auto; color: #888;">Developer dashboard</span>
                </div>
                <div class="endpoint">
                    <span class="method method-get">GET</span>
                    <span>/api/swagger/</span>
                    <span style="margin-left: auto; color: #888;">API documentation</span>
                </div>
            </div>
        </div>
        <script>
            async function checkHealth() {
                const healthStatus = document.getElementById('health-status');
                const lastUpdated = document.getElementById('last-updated');
                healthStatus.innerHTML = '<div class="loading"></div> Checking API health...';
                try {
                    const response = await fetch('/api/health');
                    const data = await response.json();
                    let statusClass = 'status-healthy';
                    if (data.status === 'unhealthy') statusClass = 'status-unhealthy';
                    if (data.status === 'degraded') statusClass = 'status-degraded';
                    let html = `<div class="status-item ${statusClass}">
                        <span>Overall Status</span>
                        <span class="status-badge badge-${data.status === 'healthy' ? 'healthy' : data.status === 'degraded' ? 'degraded' : 'unhealthy'}">${data.status.toUpperCase()}</span>
                    </div>`;
                    for (const [service, info] of Object.entries(data.services)) {
                        const serviceStatusClass = info.status === 'healthy' ? 'status-healthy' : 'status-unhealthy';
                        const badgeClass = info.status === 'healthy' ? 'badge-healthy' : 'badge-unhealthy';
                        html += `<div class="status-item ${serviceStatusClass}">
                            <span>${service.replace('_', ' ').toUpperCase()}</span>
                            <div>
                                ${info.response_time_ms ? `<small style="color: #888; margin-right: 10px;">${info.response_time_ms}ms</small>` : ''}
                                ${info.count !== undefined ? `<small style="color: #888; margin-right: 10px;">${info.count} items</small>` : ''}
                                ${info.total_count !== undefined ? `<small style="color: #888; margin-right: 10px;">${info.total_count} total</small>` : ''}
                                <span class="status-badge ${badgeClass}">${info.status.toUpperCase()}</span>
                            </div>
                        </div>`;
                    }
                    healthStatus.innerHTML = html;
                    lastUpdated.innerHTML = `Last updated: ${new Date(data.timestamp).toLocaleString()}`;
                } catch (error) {
                    healthStatus.innerHTML = `<div class="status-item status-unhealthy">
                        <span>Connection Error</span>
                        <span class="status-badge badge-unhealthy">FAILED</span>
                    </div>`;
                    lastUpdated.innerHTML = `Last updated: ${new Date().toLocaleString()} (Error: ${error.message})`;
                }
            }
            // Check health on page load only
            document.addEventListener('DOMContentLoaded', checkHealth);
        </script>
    </body>
    </html>
    '''

@dashboard_bp.route('/api/health')
def api_health():
    """
    API health check endpoint that tests all database connections
    """
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
    
    # Test study-spots endpoint
    try:
        start_time = time.time()
        # Simulate internal API call
        lecture_halls = get_lecture_halls()
        cafes = get_cafes()
        libraries = get_libraries()
        
        # Add type attribute to distinguish between categories
        lecture_halls_with_type = [{"type": "lecture_hall", **hall} for hall in lecture_halls]
        cafes_with_type = [{"type": "cafe", **cafe} for cafe in cafes]
        libraries_with_type = [{"type": "library", **library} for library in libraries]
        
        # Combine all into a single list
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
    
    return jsonify(health_status)
