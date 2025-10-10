#!/usr/bin/env python3
"""
Flask Application Initialization Script
This script initializes the database for the Flask application.
"""

import os
import sys

def main():
    """Initialize the Flask application database"""
    print("=" * 60)
    print("N.C.A.T.S Flask Application - Database Initialization")
    print("=" * 60)
    print()
    
    # Check if requirements are installed
    try:
        from app import app, db
        from models import User, Application, PasswordResetToken
    except ImportError as e:
        print("ERROR: Failed to import Flask application modules.")
        print(f"Details: {e}")
        print()
        print("Please install requirements first:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    # Create database
    print("Creating database tables...")
    try:
        with app.app_context():
            db.create_all()
            tables = list(db.metadata.tables.keys())
            print(f"✓ Successfully created {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
    except Exception as e:
        print(f"ERROR: Failed to create database: {e}")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("Database initialized successfully!")
    print()
    print("Next steps:")
    print("  1. Configure your .env file with appropriate settings")
    print("  2. Run the application: python app.py")
    print("  3. Access the application at: http://localhost:5000")
    print("=" * 60)

if __name__ == '__main__':
    main()
