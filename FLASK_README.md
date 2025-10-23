# Flask Web Application

This directory contains the Flask web application for N.C.A.T.S (Nell's Carpool and Transportation Services) with **user authentication and authorization**.

## Features

- **User Registration**: Create new user accounts with secure password hashing
- **User Login/Logout**: Authenticate users with session-based authentication
- **Protected Routes**: Access control for authenticated users only
- **Secure Password Storage**: Passwords are hashed using Werkzeug's security utilities
- **Session Management**: Secure session handling with Flask sessions
- **Flash Messages**: User-friendly feedback for actions (login, registration, errors)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Secret Key

For production use, set a strong secret key using an environment variable:

```bash
export SECRET_KEY='your-very-strong-secret-key-here'
```

Generate a strong secret key using:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Debug Mode

Debug mode is enabled by default for development. To disable it:

```bash
export FLASK_DEBUG=0
```

**Important**: Never run Flask with debug mode enabled in production!

## Running the Application

### Development Server

To run the Flask application in development mode:

```bash
python run.py
```

The application will start on `http://localhost:5000`

Alternatively, you can use Flask's built-in command:

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

### Production Server

For production deployment, use a production-grade WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

**Important Security Note**: Always set `FLASK_DEBUG=0` and use a strong `SECRET_KEY` in production.

## Application Structure

```
.
├── app/
│   ├── __init__.py          # Application factory and main routes
│   ├── auth.py              # Authentication routes (login, register, logout)
│   ├── models.py            # User model and data storage
│   ├── static/              # Static files (CSS, JS, images)
│   │   └── style.css        # Main stylesheet
│   └── templates/           # HTML templates
│       ├── base.html        # Base template with navigation
│       ├── index.html       # Welcome page
│       ├── login.html       # Login page
│       ├── register.html    # Registration page
│       └── dashboard.html   # Protected dashboard (requires login)
├── run.py                   # Application entry point
├── test_auth.py             # Authorization tests
├── requirements.txt         # Python dependencies
└── FLASK_README.md          # This file
```

## Available Routes

### Public Routes
- **`/`** - Welcome page with application information
- **`/login`** - User login page
- **`/register`** - User registration page
- **`/api/welcome`** - JSON API endpoint returning a welcome message

### Protected Routes (Authentication Required)
- **`/dashboard`** - User dashboard (only accessible when logged in)

### Authentication Actions
- **`/logout`** - Logout the current user

## Using the Application

### 1. Register a New Account

1. Navigate to `http://localhost:5000/register`
2. Enter a username (at least 3 characters)
3. Optionally enter an email address
4. Enter a password (at least 6 characters)
5. Confirm your password
6. Click "Register"

### 2. Login

1. Navigate to `http://localhost:5000/login`
2. Enter your username and password
3. Click "Login"
4. You'll be redirected to the dashboard

### 3. Access Protected Content

Once logged in, you can access the dashboard at `/dashboard`. If you try to access it without logging in, you'll be redirected to the login page.

### 4. Logout

Click the "Logout" link in the navigation bar or visit `/logout` directly.

## API Examples

### Welcome API Endpoint

```bash
curl http://localhost:5000/api/welcome
```

Response:
```json
{
  "message": "Welcome to N.C.A.T.S - Nell's Carpool and Transportation Services",
  "status": "success"
}
```

## Testing

The application includes comprehensive tests for all authentication functionality.

### Running Tests

```bash
python test_auth.py
```

Or with verbose output:

```bash
python test_auth.py -v
```

### Test Coverage

Tests include:
- User model (password hashing, verification, serialization)
- User storage (add, retrieve, check existence)
- Registration (success, validation, duplicate users)
- Login (success, invalid credentials)
- Protected routes (access control)
- Logout functionality

## Security Features

1. **Password Hashing**: All passwords are hashed using Werkzeug's security utilities (PBKDF2)
2. **Session Security**: Flask sessions with secret key for tamper protection
3. **CSRF Protection**: Built into Flask forms (can be enhanced with Flask-WTF)
4. **Input Validation**: Username and password requirements enforced
5. **Secure Cookies**: Session cookies are httpOnly by default

## Data Storage

User data is stored in a JSON file (`users.json`) in the application root directory. This file:
- Contains usernames, hashed passwords, and optional email addresses
- Is automatically created on first user registration
- Should be backed up regularly in production
- Is excluded from version control (in `.gitignore`)

**Note**: For production use, consider migrating to a proper database system like PostgreSQL or SQLite.

## Best Practices

- Always use a virtual environment to avoid dependency conflicts
- Keep your `requirements.txt` updated
- Never commit sensitive data (API keys, passwords, secret keys) to version control
- Use environment variables for configuration
- Set a strong `SECRET_KEY` in production
- Disable debug mode in production
- Use HTTPS in production to protect credentials in transit
- Implement rate limiting for authentication endpoints
- Consider adding email verification for new accounts
- Implement password reset functionality
- Add logging for security events
- Test your application thoroughly before deploying to production

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, you can specify a different port:

```bash
flask run --port 5001
```

Or modify the `run.py` file to use a different port.

### Module Not Found

Make sure you've activated your virtual environment and installed all dependencies:

```bash
pip install -r requirements.txt
```

### Can't Access Dashboard

Make sure you're logged in. If you see a redirect to the login page, your session may have expired. Log in again.

### User Data Lost

If you delete or corrupt the `users.json` file, all user accounts will be lost. The file will be recreated automatically on the next registration, but existing users will need to re-register.

## Future Enhancements

Potential improvements for the authorization system:

- Migrate to SQLAlchemy for better database management
- Add Flask-Login for more robust session management
- Implement password reset via email
- Add email verification for new accounts
- Implement "Remember Me" functionality
- Add user roles and permissions
- Implement rate limiting for authentication endpoints
- Add two-factor authentication (2FA)
- Add OAuth2 social login (Google, GitHub, etc.)
- Implement account lockout after failed login attempts

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Quickstart](https://flask.palletsprojects.com/en/3.0.x/quickstart/)
- [Deploying Flask Applications](https://flask.palletsprojects.com/en/3.0.x/deploying/)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/en/3.0.x/utils/#module-werkzeug.security)
- [Flask Sessions](https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions)

## License

This project is licensed under the Boost Software License - Version 1.0. See the LICENSE file for details.
