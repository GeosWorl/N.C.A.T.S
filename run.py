"""
N.C.A.T.S Flask Application Entry Point
"""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Debug mode should only be enabled in development
    # Set FLASK_DEBUG=0 in production environments
    debug_mode = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
