# Flask Web Application for N.C.A.T.S

This Flask web application provides a user interface for N.C.A.T.S (Nell's Carpool and Transportation Services) with smart contract integration.

## Features

- **User Authentication**: Secure registration and login with bcrypt password hashing
- **Password Reset**: Email-based password reset functionality
- **User Profiles**: View profile information and application history
- **Application Submission**: Submit applications with resume upload (local or AWS S3)
- **Smart Contract Integration**: Interact with the Ethereum smart contract
- **Security Features**:
  - CSRF protection
  - Rate limiting
  - Session management
  - Input validation
  - Optional reCAPTCHA support

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Node.js and npm (for smart contract development)

### Setup

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
- `SECRET_KEY`: Flask secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- `DATABASE_URL`: Database connection string (default: SQLite)

Optional configuration:
- Email settings for password reset (`MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD`)
- reCAPTCHA keys for bot protection
- AWS S3 credentials for cloud file storage
- Ethereum/Infura configuration for smart contract interaction

3. Initialize the database:

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

Or use Flask-Migrate:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Running the Application

### Development

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Production (with Gunicorn)

```bash
gunicorn app:app --config gunicorn_config.py
```

### Heroku Deployment

The application includes a `Procfile` for Heroku deployment:

```bash
heroku create your-app-name
heroku config:set SECRET_KEY=your_secret_key
heroku config:set DATABASE_URL=your_database_url
# Set other environment variables
git push heroku main
```

## Project Structure

```
.
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── Procfile                    # Heroku deployment config
├── gunicorn_config.py         # Gunicorn configuration
├── templates/                  # HTML templates
│   ├── index.html             # Home page with login/register
│   ├── profile.html           # User profile page
│   ├── reset_request.html     # Password reset request
│   └── reset_password.html    # Password reset form
├── static/                     # Static files
│   └── styles.css             # Application styles
├── uploads/                    # Local file uploads (created automatically)
└── instance/                   # SQLite database location (created automatically)
```

## Database Models

### User
- id: Integer (Primary Key)
- username: String (Unique)
- email: String (Unique)
- password: String (Hashed)
- created_at: DateTime

### Application
- id: Integer (Primary Key)
- name: String
- email: String
- resume_path: String
- submitted_at: DateTime
- user_id: Foreign Key to User

### PasswordResetToken
- id: Integer (Primary Key)
- token: String (Unique)
- user_id: Foreign Key to User
- expires_at: DateTime
- created_at: DateTime

## Smart Contract Integration

The application integrates with the ContractAgreement smart contract deployed at:
`0x721ED067e04dC811c94c9A0C45b6160De799E2C0`

To enable smart contract features:
1. Set `INFURA_URL` in your `.env` file
2. Set `CONTRACT_ADDRESS` (defaults to the deployed contract)
3. Update the `contract_abi` in `app.py` with the compiled contract ABI

The `interact_with_contract()` function in `app.py` provides a template for smart contract interactions.

## Security Considerations

1. **Never commit sensitive data**: Keep your `.env` file out of version control
2. **Use strong secret keys**: Generate secure random keys for production
3. **Enable HTTPS**: Set `SESSION_COOKIE_SECURE=True` in production with HTTPS
4. **Configure email**: Set up proper email credentials for password reset
5. **Enable reCAPTCHA**: Add reCAPTCHA keys to prevent bot attacks
6. **Rate limiting**: Configured by default to prevent abuse
7. **Database backups**: Regularly backup your production database

## Development vs Production

### Development Settings
- `FLASK_DEBUG=True`
- `SESSION_COOKIE_SECURE=False`
- SQLite database
- Skip reCAPTCHA verification if not configured
- Local file uploads

### Production Settings
- `FLASK_DEBUG=False`
- `SESSION_COOKIE_SECURE=True` (with HTTPS)
- PostgreSQL or other production database
- Full reCAPTCHA verification
- AWS S3 for file uploads
- Use Gunicorn as WSGI server

## Monitoring and Logging

The application uses Python's logging module. Logs include:
- User authentication events
- Application submissions
- Password reset requests
- Errors and exceptions

For production monitoring:
- Use services like Sentry for error tracking
- Set up application performance monitoring (APM)
- Monitor database performance
- Track rate limiting violations

## License

Boost Software License - Version 1.0

## Author

Cory K Washington (Geo) - Owner and Creator of N.C.A.T.S
