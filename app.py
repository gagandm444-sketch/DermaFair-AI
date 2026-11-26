# -*- coding: utf-8 -*-
"""
DermaFair AI - Flask Application Entrypoint
Explainable Multi-Class Skin Disease Classification with Fairness Analysis Across Skin Tones.
"""

import os
import sys
from flask import Flask, render_template, jsonify

# Add project root to Python module search path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config import Config
from backend.routes.view_routes import view_bp
from backend.routes.api_routes import api_bp
from backend.database.db import init_db

def create_app(config_class=Config):
    # Configure template and static directories
    template_dir = os.path.join(BASE_DIR, 'templates') if os.path.exists(os.path.join(BASE_DIR, 'templates')) else os.path.join(BASE_DIR, 'frontend', 'templates')
    static_dir = os.path.join(BASE_DIR, 'static') if os.path.exists(os.path.join(BASE_DIR, 'static')) else os.path.join(BASE_DIR, 'frontend', 'static')

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir
    )

    app.config.from_object(config_class)

    # Ensure required runtime directories exist
    upload_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Initialize SQLite database
    init_db()

    # Register blueprints
    app.register_blueprint(view_bp)
    app.register_blueprint(api_bp)

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('base.html', active_page=''), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({'success': False, 'error': 'File exceeds the maximum 16MB upload limit.'}), 413

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'success': False, 'error': 'Internal server error occurred.'}), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 65)
    print("DermaFair AI Clinical Application Server Starting...")
    print("Supported Classes: 23 Dermatological Families")
    print("Explainable AI: Grad-CAM Activated")
    print("Fairness Audit: Fitzpatrick I-VI Stratified")
    print("Local URL: http://127.0.0.1:{}".format(port))
    print("=" * 65)
    app.run(host='0.0.0.0', port=port, debug=True)
