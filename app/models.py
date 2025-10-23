"""
User model and data management for N.C.A.T.S
"""
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """User model for authentication"""
    
    def __init__(self, username, password_hash=None, email=None):
        self.username = username
        self.password_hash = password_hash
        self.email = email
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary for storage"""
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            'email': self.email
        }
    
    @staticmethod
    def from_dict(data):
        """Create user from dictionary"""
        return User(
            username=data['username'],
            password_hash=data['password_hash'],
            email=data.get('email')
        )


class UserStore:
    """Simple JSON-based user storage"""
    
    def __init__(self, storage_path='users.json'):
        self.storage_path = storage_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create storage file if it doesn't exist"""
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump({}, f)
    
    def _load_users(self):
        """Load all users from storage"""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                return {username: User.from_dict(user_data) 
                       for username, user_data in data.items()}
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_users(self, users):
        """Save all users to storage"""
        data = {username: user.to_dict() 
               for username, user in users.items()}
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_user(self, username):
        """Get user by username"""
        users = self._load_users()
        return users.get(username)
    
    def add_user(self, user):
        """Add new user to storage"""
        users = self._load_users()
        if user.username in users:
            return False
        users[user.username] = user
        self._save_users(users)
        return True
    
    def user_exists(self, username):
        """Check if user exists"""
        users = self._load_users()
        return username in users
