# Flask Web Application Implementation Summary

## Overview

This implementation adds a complete Flask web application to the N.C.A.T.S repository, providing a user-friendly web interface for Nell's Carpool and Transportation Services with smart contract integration.

## Features Implemented

### 1. User Authentication System
- **User Registration**: Secure user registration with username, email, and password
- **User Login**: Session-based authentication with bcrypt password hashing
- **User Logout**: Secure logout functionality
- **Password Reset**: Email-based password reset with time-limited tokens (1-hour expiration)

### 2. User Profiles
- View user profile information (username, email, registration date)
- Application history tracking
- View all previously submitted applications

### 3. Application Submission
- Secure form for submitting applications
- Resume upload with file validation (PDF, DOC, DOCX only)
- Support for both local file storage and AWS S3 cloud storage
- Applications linked to user accounts

### 4. Security Features
- **CSRF Protection**: Flask-WTF provides CSRF tokens for all forms
- **Rate Limiting**: Prevents abuse with configurable rate limits
  - 10 login attempts per minute
  - 10 registration attempts per minute
  - 5 application submissions per hour
  - 10 password reset requests per hour
- **Input Validation**: Username validation (alphanumeric + underscore only)
- **Password Hashing**: Bcrypt for secure password storage
- **Session Security**: Secure session cookies, configurable for HTTPS
- **Optional reCAPTCHA**: Bot protection for login and registration

### 5. Smart Contract Integration
- Web3.py integration for Ethereum interaction
- Configured to work with the deployed ContractAgreement smart contract
- Template function for contract interaction (`interact_with_contract()`)

### 6. Database Models
Three main models implemented with SQLAlchemy:
- **User**: Stores user credentials and profile information
- **Application**: Tracks submitted applications with resume links
- **PasswordResetToken**: Manages password reset tokens with expiration

### 7. Responsive UI
- Modern, professional CSS design
- Responsive layout for mobile and desktop
- Color-coded flash messages (success, error, info)
- Clean navigation and user experience

## Files Added

### Core Application Files
1. **app.py** (424 lines)
   - Main Flask application
   - All routes and business logic
   - Security configuration
   - Smart contract integration setup

2. **models.py** (49 lines)
   - SQLAlchemy database models
   - User, Application, PasswordResetToken

3. **requirements.txt** (15 packages)
   - Flask and extensions
   - Database support
   - Security libraries
   - Web3 integration

### Templates (HTML)
4. **templates/index.html** (125 lines)
   - Home page with login/register forms
   - Application submission form
   - Dynamic content based on login status

5. **templates/profile.html** (74 lines)
   - User profile display
   - Application history table

6. **templates/reset_request.html** (48 lines)
   - Password reset request form

7. **templates/reset_password.html** (51 lines)
   - New password entry form

### Static Files
8. **static/styles.css** (269 lines)
   - Modern, responsive CSS
   - Gradient backgrounds
   - Professional styling for forms and tables

### Configuration Files
9. **Procfile**
   - Heroku deployment configuration
   - Gunicorn WSGI server

10. **gunicorn_config.py** (23 lines)
    - Production server configuration
    - Worker processes and timeouts

11. **.env.example** (updated)
    - Environment variable template
    - Flask configuration options
    - Smart contract settings

12. **.gitignore** (updated)
    - Python/Flask specific ignores
    - Database files
    - Virtual environments

### Utility Scripts
13. **init_db.py** (53 lines)
    - Database initialization helper
    - User-friendly setup script
    - Error handling and instructions

### Documentation
14. **FLASK_README.md** (203 lines)
    - Comprehensive Flask app documentation
    - Installation instructions
    - Configuration guide
    - Security best practices
    - Deployment instructions

15. **README.md** (updated)
    - Integrated Flask app into main README
    - Quick start for both smart contract and Flask app
    - Project structure overview

## Technical Specifications

### Dependencies
- **Flask 3.0.0**: Web framework
- **Flask-SQLAlchemy 3.1.1**: Database ORM
- **Flask-Migrate 4.0.5**: Database migrations
- **Flask-WTF 1.2.1**: Form handling and CSRF protection
- **Flask-Mail 0.9.1**: Email functionality
- **Flask-Limiter 3.5.0**: Rate limiting
- **bcrypt 4.1.2**: Password hashing
- **web3 6.11.3**: Ethereum integration
- **boto3 1.34.11**: AWS S3 support
- **gunicorn 21.2.0**: Production WSGI server

### Database
- SQLite for development (default)
- PostgreSQL/MySQL support for production
- Automatic path handling for cross-platform compatibility
- Three tables: users, applications, password_reset_tokens

### Security Best Practices
- All passwords hashed with bcrypt
- CSRF protection on all forms
- Rate limiting on sensitive endpoints
- Session cookie security
- Input validation and sanitization
- Optional reCAPTCHA integration
- Secure file upload validation

### Smart Contract Integration
- Connects to Ethereum via Infura
- Configured for ContractAgreement at 0x721ED067e04dC811c94c9A0C45b6160De799E2C0
- Ready to interact with contract functions
- Template for transaction signing and submission

## Setup Instructions

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python3 init_db.py

# Run application
python app.py
```

### Production Deployment
```bash
# Use PostgreSQL database
export DATABASE_URL=postgresql://user:pass@host/db

# Configure email for password reset
export MAIL_SERVER=smtp.gmail.com
export MAIL_USERNAME=your_email@gmail.com
export MAIL_PASSWORD=your_app_password

# Enable HTTPS session cookies
export SESSION_COOKIE_SECURE=True

# Deploy with Gunicorn
gunicorn app:app --config gunicorn_config.py
```

## Testing Results

All functionality tested successfully:
- ✓ Database initialization
- ✓ User creation and retrieval
- ✓ Password hashing and verification
- ✓ Route accessibility (index, profile, reset pages)
- ✓ Flask application configuration
- ✓ CSRF protection enabled
- ✓ Form validation

## Future Enhancements

Potential additions for future development:
1. Email verification for new registrations
2. Two-factor authentication (2FA)
3. Admin dashboard for managing applications
4. Real-time smart contract status updates
5. Enhanced analytics and reporting
6. API endpoints for mobile app integration
7. Social authentication (OAuth)
8. Advanced role-based access control

## Compatibility

- Python 3.8+
- All major browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive
- Cross-platform (Windows, macOS, Linux)

## License

This implementation follows the repository's Boost Software License - Version 1.0

## Author

Implementation by GitHub Copilot for Cory K Washington (Geo)
Owner of N.C.A.T.S - Nell's Carpool and Transportation Services
