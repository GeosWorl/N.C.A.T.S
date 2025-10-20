# Flask Web Application

This directory contains the Flask web application for N.C.A.T.S (Nell's Carpool and Transportation Services).

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

## Application Structure

```
.
├── app/
│   ├── __init__.py          # Application factory and routes
│   ├── static/              # Static files (CSS, JS, images)
│   │   └── style.css        # Main stylesheet
│   └── templates/           # HTML templates
│       └── index.html       # Welcome page template
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── FLASK_README.md          # This file
```

## Available Routes

- **`/`** - Main welcome page with UI
- **`/api/welcome`** - JSON API endpoint returning a welcome message

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

## Configuration

The application uses a default configuration suitable for development. For production:

1. Set a strong `SECRET_KEY` in the application configuration
2. Set `debug=False` when running the application
3. Use environment variables for sensitive configuration
4. Consider using a configuration file or environment-based config

## Best Practices

- Always use a virtual environment to avoid dependency conflicts
- Keep your `requirements.txt` updated
- Never commit sensitive data (API keys, passwords) to version control
- Use environment variables for configuration
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

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Quickstart](https://flask.palletsprojects.com/en/3.0.x/quickstart/)
- [Deploying Flask Applications](https://flask.palletsprojects.com/en/3.0.x/deploying/)

## License

This project is licensed under the Boost Software License - Version 1.0. See the LICENSE file for details.
