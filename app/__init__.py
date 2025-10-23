"""
Flask application for N.C.A.T.S (Nell's Carpool and Transportation Services)
"""
import os
from flask import Flask, render_template, session
from app.auth import auth_bp, login_required


def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Register authentication blueprint
    app.register_blueprint(auth_bp)
    
    @app.route('/')
    def index():
        """Welcome route"""
        return render_template('index.html')
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """Protected dashboard route - requires authentication"""
        username = session.get('username')
        return render_template('dashboard.html', username=username)
    
    @app.route('/api/welcome')
    def api_welcome():
        """API endpoint that returns a welcome message"""
        return {
            'message': 'Welcome to N.C.A.T.S - Nell\'s Carpool and Transportation Services',
            'status': 'success'
        }
    
    return app
