"""
Flask application for N.C.A.T.S (Nell's Carpool and Transportation Services)
"""
from flask import Flask, render_template


def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev'  # Change this in production
    
    @app.route('/')
    def index():
        """Welcome route"""
        return render_template('index.html')
    
    @app.route('/api/welcome')
    def api_welcome():
        """API endpoint that returns a welcome message"""
        return {
            'message': 'Welcome to N.C.A.T.S - Nell\'s Carpool and Transportation Services',
            'status': 'success'
        }
    
    return app
