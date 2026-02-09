# SHIELD AI - TITAN HIVE C2
# ---------------------------------------------------
# ARCHITECTURE NOTE:
# This repository contains the reference source code.
# Critical security modules and API keys have been
# decoupled for safety. Please use the compiled
# 'Judge Edition' binary for the functional demo.
# ---------------------------------------------------

"""
Titan Hive C2 - Command & Control Server
Reference implementation for the Shield AI platform.
"""

import os
import sys
import time
import threading
from flask import Flask, render_template, request, jsonify

# Core Intelligence Module (Decoupled for Security)
from hive_core.legacy_brain import TitanNeuralEngine  # noqa: F401

# =========================================================================
# ⚙️ CONFIGURATION
# =========================================================================
SECRET_KEY = os.environ.get('HIVE_SECRET_KEY', 'development-key')
DATABASE_URI = os.environ.get('HIVE_DB_URI', 'sqlite:///instance/hive.db')

# =========================================================================
# 🏗️ APPLICATION FACTORY
# =========================================================================
def create_app():
    """Initialize the Titan Hive C2 Server."""
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Register blueprints
    from hive_core.routes import web_bp
    from hive_core.api import api_bp
    
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    return app

# =========================================================================
# 🚀 ENTRY POINT
# =========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  TITAN HIVE C2 - Reference Implementation")
    print("=" * 60)
    print("  [!] This is the public reference code.")
    print("  [!] For the functional demo, use the Judge Edition EXE.")
    print("=" * 60)
    
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
