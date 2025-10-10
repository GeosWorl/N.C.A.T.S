from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
import os
import boto3
from botocore.exceptions import ClientError
import bcrypt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from web3 import Web3
import logging
import re
import secrets
import requests
from flask_mail import Mail, Message

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_fallback_secret_key')

# Database configuration - handle relative paths for SQLite
database_url = os.getenv('DATABASE_URL')
if not database_url or database_url.startswith('sqlite:///instance/'):
    # Use absolute path for SQLite if relative path is specified
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'carpool.db')
    database_url = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600
app.config['WTF_CSRF_ENABLED'] = True
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

# Import models after Flask app is created
from models import db, User, Application, PasswordResetToken

db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Rate limiter
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

# AWS S3 setup (optional)
s3_client = None
S3_BUCKET = os.getenv('S3_BUCKET')
if os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY'):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

# Ensure local upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('instance', exist_ok=True)

# Ethereum setup
w3 = None
contract = None
if os.getenv('INFURA_URL'):
    w3 = Web3(Web3.HTTPProvider(os.getenv('INFURA_URL')))
    contract_address = os.getenv('CONTRACT_ADDRESS', '0x721ED067e04dC811c94c9A0C45b6160De799E2C0')
    # Contract ABI would be loaded from compiled contract
    contract_abi = []  # Replace with actual ABI from contracts/ContractAgreement.sol
    if contract_abi:
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# CSRF-protected forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    recaptcha = StringField()  # Hidden field for reCAPTCHA response
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    recaptcha = StringField()  # Hidden field for reCAPTCHA response
    submit = SubmitField('Create Account')

class ApplyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    resume = FileField('Upload Resume', validators=[DataRequired()])
    submit = SubmitField('Submit Application')

class ResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

# Helper function to check if user is logged in
def is_logged_in():
    return 'user_id' in session

# Input validation for username
def is_valid_username(username):
    return bool(re.match(r'^[a-zA-Z0-9_]+$', username))

# Verify reCAPTCHA
def verify_recaptcha(recaptcha_response):
    if not app.config['RECAPTCHA_PRIVATE_KEY']:
        return True  # Skip in local dev if not configured
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': app.config['RECAPTCHA_PRIVATE_KEY'],
            'response': recaptcha_response,
            'remoteip': get_remote_address()
        }
    )
    return response.json().get('success', False)

@app.route('/')
def index():
    username = None
    if is_logged_in():
        user = User.query.get(session['user_id'])
        username = user.username if user else None
    return render_template(
        'index.html',
        is_logged_in=is_logged_in(),
        username=username,
        login_form=LoginForm(),
        register_form=RegisterForm(),
        apply_form=ApplyForm(),
        reset_request_form=ResetRequestForm(),
        recaptcha_site_key=app.config['RECAPTCHA_PUBLIC_KEY']
    )

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            recaptcha_response = request.form.get('g-recaptcha-response')

            if not verify_recaptcha(recaptcha_response):
                flash('reCAPTCHA verification failed.', 'error')
                return redirect(url_for('index'))

            if not is_valid_username(username):
                flash('Username can only contain letters, numbers, and underscores.', 'error')
                return redirect(url_for('index'))

            user = User.query.filter_by(username=username).first()

            if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                session['user_id'] = user.id
                session.permanent = True
                logger.info(f"User logged in: {username}")
                flash(f'Welcome back, {username}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.', 'error')
                return redirect(url_for('index'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field.capitalize()}: {error}", 'error')
            return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        flash('An error occurred during login. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    try:
        session.pop('user_id', None)
        logger.info("User logged out")
        flash('You have been logged out.', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        flash('An error occurred during logout. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
@limiter.limit("10 per minute")
def register():
    try:
        form = RegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            recaptcha_response = request.form.get('g-recaptcha-response')

            if not verify_recaptcha(recaptcha_response):
                flash('reCAPTCHA verification failed.', 'error')
                return redirect(url_for('index'))

            if not is_valid_username(username):
                flash('Username can only contain letters, numbers, and underscores.', 'error')
                return redirect(url_for('index'))

            if User.query.filter_by(username=username).first():
                flash('Username already exists!', 'error')
                return redirect(url_for('index'))

            if User.query.filter_by(email=email).first():
                flash('Email already registered!', 'error')
                return redirect(url_for('index'))

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            logger.info(f"New user registered: {username}")
            flash(f'Account for {username} created successfully!', 'success')
            return redirect(url_for('index'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field.capitalize()}: {error}", 'error')
            return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        flash('An error occurred during registration. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/apply', methods=['POST'])
@limiter.limit("5 per hour")
def apply():
    try:
        if not is_logged_in():
            flash('Please log in to submit an application.', 'error')
            return redirect(url_for('index'))

        form = ApplyForm()
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            resume = form.resume.data

            allowed_extensions = {'pdf', 'doc', 'docx'}
            if not '.' in resume.filename or resume.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                flash('Resume must be a PDF, DOC, or DOCX file.', 'error')
                return redirect(url_for('index'))

            filename = secure_filename(f"{session['user_id']}_{datetime.utcnow().timestamp()}_{resume.filename}")

            if S3_BUCKET and s3_client:
                try:
                    s3_client.upload_fileobj(
                        resume,
                        S3_BUCKET,
                        filename,
                        ExtraArgs={'ContentType': resume.content_type}
                    )
                    resume_path = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"
                except ClientError as e:
                    logger.error(f"S3 upload error: {str(e)}")
                    flash('Error uploading resume. Please try again.', 'error')
                    return redirect(url_for('index'))
            else:
                resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                resume.save(resume_path)

            new_application = Application(
                name=name,
                email=email,
                resume_path=resume_path,
                submitted_at=datetime.utcnow(),
                user_id=session['user_id']
            )
            db.session.add(new_application)
            db.session.commit()

            logger.info(f"New application submitted: {name}")
            flash(f'Application submitted successfully for {name}!', 'success')
            return redirect(url_for('index'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field.capitalize()}: {error}", 'error')
            return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error during application submission: {str(e)}")
        flash('An error occurred during application submission. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/profile')
def profile():
    try:
        if not is_logged_in():
            flash('Please log in to view your profile.', 'error')
            return redirect(url_for('index'))

        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('index'))

        applications = Application.query.filter_by(user_id=user.id).all()
        return render_template('profile.html', user=user, applications=applications)
    except Exception as e:
        logger.error(f"Error accessing profile: {str(e)}")
        flash('An error occurred while accessing your profile. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/reset_request', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def reset_request():
    try:
        if is_logged_in():
            return redirect(url_for('index'))

        form = ResetRequestForm()
        if form.validate_on_submit():
            email = form.email.data
            user = User.query.filter_by(email=email).first()
            if user:
                token = secrets.token_urlsafe(32)
                expires_at = datetime.utcnow() + timedelta(hours=1)
                reset_token = PasswordResetToken(user_id=user.id, token=token, expires_at=expires_at)
                db.session.add(reset_token)
                db.session.commit()

                reset_url = url_for('reset_password', token=token, _external=True)
                
                if app.config['MAIL_USERNAME']:
                    msg = Message(
                        'Password Reset Request',
                        sender=app.config['MAIL_USERNAME'],
                        recipients=[email],
                        body=f'To reset your password, click this link: {reset_url}\nThis link expires in 1 hour.'
                    )
                    mail.send(msg)
                    logger.info(f"Password reset email sent to {email}")
                    flash('A password reset link has been sent to your email.', 'success')
                else:
                    # For development without email configured
                    logger.info(f"Password reset link (dev mode): {reset_url}")
                    flash(f'Password reset link (dev mode): {reset_url}', 'info')
            else:
                flash('No account found with that email.', 'error')
            return redirect(url_for('index'))

        return render_template('reset_request.html', form=form)
    except Exception as e:
        logger.error(f"Error during password reset request: {str(e)}")
        flash('An error occurred while processing your request. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def reset_password(token):
    try:
        if is_logged_in():
            return redirect(url_for('index'))

        reset_token = PasswordResetToken.query.filter_by(token=token).first()
        if not reset_token or reset_token.expires_at < datetime.utcnow():
            flash('The password reset link is invalid or has expired.', 'error')
            return redirect(url_for('index'))

        form = ResetPasswordForm()
        if form.validate_on_submit():
            user = User.query.get(reset_token.user_id)
            if user:
                hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user.password = hashed_password
                db.session.delete(reset_token)
                db.session.commit()
                logger.info(f"Password reset for user ID {user.id}")
                flash('Your password has been reset successfully. Please log in.', 'success')
                return redirect(url_for('index'))
        return render_template('reset_password.html', form=form, token=token)
    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        flash('An error occurred while resetting your password. Please try again.', 'error')
        return redirect(url_for('index'))

# Placeholder for smart contract interaction
def interact_with_contract():
    """Interact with the deployed ContractAgreement smart contract"""
    try:
        if not contract or not w3:
            logger.warning("Smart contract not configured")
            return None
        
        # Example: Get contract details
        details = contract.functions.getContractDetails().call()
        logger.info(f"Smart contract details retrieved: {details}")
        return details
    except Exception as e:
        logger.error(f"Error in smart contract interaction: {str(e)}")
        raise

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
