"""
Medical AI Skin Diagnosis System - Flask Application Entry Point

This is the main entry point for the Flask application.
Initializes all components and starts the server.
"""

import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

from config import get_config
from api import register_blueprints
from storage import init_storage
from utils.logger import setup_logging, get_logger


def create_app(config=None):
    """
    Application factory pattern for Flask app creation.
    
    Args:
        config: Optional configuration object. If None, loads from environment.
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__, 
                static_folder='../frontend',
                static_url_path='')
    
    # Load configuration
    if config is None:
        config = get_config()
    
    app.config.from_object(config)
    
    # Setup CORS for API endpoints
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize logging
    setup_logging(app)
    logger = get_logger('app')
    
    # Initialize storage directories
    init_storage(config)
    logger.info("Storage directories initialized")
    
    # Register API blueprints
    register_blueprints(app)
    logger.info("API blueprints registered")
    
    # Serve frontend files
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        """Serve static files or fall back to index.html for SPA routing"""
        file_path = os.path.join(app.static_folder, path)
        if os.path.isfile(file_path):
            return send_from_directory(app.static_folder, path)
        # Check if it's an HTML file request
        if not '.' in path or path.endswith('.html'):
            html_path = path if path.endswith('.html') else f"{path}.html"
            html_file_path = os.path.join(app.static_folder, html_path)
            if os.path.isfile(html_file_path):
                return send_from_directory(app.static_folder, html_path)
        return send_from_directory(app.static_folder, 'index.html')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'service': 'Medical AI Skin Diagnosis System'
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'code': 404}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"Server error: {error}")
        return jsonify({'error': 'Internal server error', 'code': 500}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'code': 400}), 400
    
    logger.info(f"Application initialized - Debug: {app.debug}")
    
    return app


# Create the application instance
app = create_app()


if __name__ == '__main__':
    config = get_config()
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║     Medical AI Skin Diagnosis System                     ║
    ║     Version 1.0.0                                        ║
    ╠══════════════════════════════════════════════════════════╣
    ║     Server: http://{config.HOST}:{config.PORT}                        ║
    ║     Debug: {str(config.DEBUG).ljust(46)}║
    ╚══════════════════════════════════════════════════════════╝
    """)
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
