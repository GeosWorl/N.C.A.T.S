"""
Tests for N.C.A.T.S Flask Authorization
"""
import os
import sys
import unittest
import tempfile
import json

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import User, UserStore


class TestUser(unittest.TestCase):
    """Test User model"""
    
    def test_set_password(self):
        """Test password hashing"""
        user = User('testuser')
        user.set_password('testpassword123')
        self.assertIsNotNone(user.password_hash)
        self.assertNotEqual(user.password_hash, 'testpassword123')
    
    def test_check_password(self):
        """Test password verification"""
        user = User('testuser')
        user.set_password('testpassword123')
        self.assertTrue(user.check_password('testpassword123'))
        self.assertFalse(user.check_password('wrongpassword'))
    
    def test_to_dict(self):
        """Test user serialization"""
        user = User('testuser', email='test@example.com')
        user.set_password('testpassword123')
        user_dict = user.to_dict()
        self.assertEqual(user_dict['username'], 'testuser')
        self.assertEqual(user_dict['email'], 'test@example.com')
        self.assertIn('password_hash', user_dict)
    
    def test_from_dict(self):
        """Test user deserialization"""
        user_data = {
            'username': 'testuser',
            'password_hash': 'hashed_password',
            'email': 'test@example.com'
        }
        user = User.from_dict(user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.password_hash, 'hashed_password')
        self.assertEqual(user.email, 'test@example.com')


class TestUserStore(unittest.TestCase):
    """Test UserStore"""
    
    def setUp(self):
        """Create a temporary storage file"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.user_store = UserStore(self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_user(self):
        """Test adding a new user"""
        user = User('testuser', email='test@example.com')
        user.set_password('testpassword123')
        result = self.user_store.add_user(user)
        self.assertTrue(result)
    
    def test_add_duplicate_user(self):
        """Test adding a duplicate user"""
        user = User('testuser', email='test@example.com')
        user.set_password('testpassword123')
        self.user_store.add_user(user)
        
        # Try to add the same user again
        duplicate_user = User('testuser', email='another@example.com')
        duplicate_user.set_password('differentpassword')
        result = self.user_store.add_user(duplicate_user)
        self.assertFalse(result)
    
    def test_get_user(self):
        """Test retrieving a user"""
        user = User('testuser', email='test@example.com')
        user.set_password('testpassword123')
        self.user_store.add_user(user)
        
        retrieved_user = self.user_store.get_user('testuser')
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, 'testuser')
        self.assertEqual(retrieved_user.email, 'test@example.com')
    
    def test_user_exists(self):
        """Test checking if user exists"""
        user = User('testuser', email='test@example.com')
        user.set_password('testpassword123')
        self.user_store.add_user(user)
        
        self.assertTrue(self.user_store.user_exists('testuser'))
        self.assertFalse(self.user_store.user_exists('nonexistent'))


class TestAuthRoutes(unittest.TestCase):
    """Test authentication routes"""
    
    def setUp(self):
        """Set up test client"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        self.client = self.app.test_client()
        
        # Create a temporary storage file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        
        # Monkey patch the user store to use temp file
        from app import auth
        auth.user_store = UserStore(self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_register_page(self):
        """Test registration page loads"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)
    
    def test_login_page(self):
        """Test login page loads"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_registration_success(self):
        """Test successful user registration"""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)
    
    def test_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'differentpassword'
        })
        self.assertIn(b'Passwords do not match', response.data)
    
    def test_registration_short_password(self):
        """Test registration with short password"""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'short',
            'confirm_password': 'short'
        })
        self.assertIn(b'Password must be at least 6 characters', response.data)
    
    def test_login_success(self):
        """Test successful login"""
        # First register a user
        self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        
        # Then try to login
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully logged in', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/login', data={
            'username': 'nonexistent',
            'password': 'wrongpassword'
        })
        self.assertIn(b'Invalid username or password', response.data)
    
    def test_protected_route_requires_login(self):
        """Test that dashboard requires authentication"""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect
        
    def test_protected_route_with_login(self):
        """Test accessing dashboard after login"""
        # Register and login
        self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Access protected route
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'testuser', response.data)
    
    def test_logout(self):
        """Test logout functionality"""
        # Register and login
        self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'logged out', response.data)
        
        # Try to access protected route after logout
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # Should redirect
    
    def test_open_redirect_protection(self):
        """Test that open redirects are prevented"""
        # Register a user
        self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        
        # Try to login with malicious redirect URL
        response = self.client.post('/login?next=https://evil.com', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=False)
        
        # Should redirect to dashboard, not the evil URL
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.location)
        self.assertNotIn('evil.com', response.location)


if __name__ == '__main__':
    unittest.main()
