# File: hive_core/__init__.py
# Shield Hive - Flask Application Factory (PyInstaller Compatible)

import os
import sys
from flask import Flask
from .models import db


def get_base_path():
    """
    Get the base path for resources.
    Handles both normal execution and PyInstaller frozen mode.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled EXE - use the temp extraction folder
        return sys._MEIPASS
    else:
        # Running as script - use project root
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_instance_path():
    """
    Get the instance path for database.
    When frozen, use executable's directory so data persists.
    """
    if getattr(sys, 'frozen', False):
        # Running as EXE - put database next to the EXE
        return os.path.dirname(sys.executable)
    else:
        # Running as script - use instance folder
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'instance')


def create_app(config_override=None):
    """
    Flask Application Factory for Shield Hive C2 Server.
    """
    base_dir = get_base_path()
    instance_path = get_instance_path()
    template_path = os.path.join(base_dir, 'templates')
    static_path = os.path.join(base_dir, 'static')
    
    # Debug output for troubleshooting
    print(f"[HIVE] Base path: {base_dir}")
    print(f"[HIVE] Instance path: {instance_path}")
    print(f"[HIVE] Templates: {template_path}")
    
    # Create instance directory if it doesn't exist
    os.makedirs(instance_path, exist_ok=True)
    
    # Create Flask app with correct paths
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder=template_path,
        static_folder=static_path if os.path.exists(static_path) else None
    )
    
    # Configuration
    db_path = os.path.join(instance_path, 'titan_hive_v2.db')
    print(f"[HIVE] Database: {db_path}")
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('HIVE_SECRET_KEY', 'TITAN_HIVE_SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
    )
    
    if config_override:
        app.config.from_mapping(config_override)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register API blueprint
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Register Web blueprint (dashboard routes)
    from .routes import web_bp
    app.register_blueprint(web_bp)
    
    # Create tables (safe for existing data)
    with app.app_context():
        db.create_all()
    
    # Health check
    @app.route('/health')
    def health_check():
        return {'status': 'online', 'service': 'shield_hive'}, 200
    
    # Dashboard-friendly API routes (without /v1 prefix)
    from .api import ai_brief, get_agents
    app.add_url_rule('/api/ai_brief', 'api_ai_brief', ai_brief)
    app.add_url_rule('/api/agents', 'api_agents', get_agents)
    
    return app
