"""
Authentication module for user management
"""
import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta

# Simple file-based user storage (in production, use a proper database)
USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')
SESSIONS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'sessions.json')

def ensure_data_files():
    """Ensure user and session data files exist"""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    
    if not os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, 'w') as f:
            json.dump({}, f)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

def load_users():
    """Load users from file"""
    ensure_data_files()
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    """Save users to file"""
    ensure_data_files()
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_sessions():
    """Load sessions from file"""
    ensure_data_files()
    try:
        with open(SESSIONS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_sessions(sessions):
    """Save sessions to file"""
    ensure_data_files()
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(sessions, f, indent=2)

def register_user(user_data):
    """Register a new user"""
    users = load_users()
    
    # Check if email already exists
    if user_data['email'] in users:
        return {'success': False, 'error': 'Email already registered'}
    
    # Validate required fields
    required_fields = ['firstName', 'lastName', 'email', 'age', 'gender', 'profession', 'password']
    for field in required_fields:
        if field not in user_data or not user_data[field]:
            return {'success': False, 'error': f'Missing required field: {field}'}
    
    # Validate age
    try:
        age = int(user_data['age'])
        if age < 13 or age > 120:
            return {'success': False, 'error': 'Age must be between 13 and 120'}
    except ValueError:
        return {'success': False, 'error': 'Invalid age format'}
    
    # Validate password length
    if len(user_data['password']) < 6:
        return {'success': False, 'error': 'Password must be at least 6 characters long'}
    
    # Create user record
    user_record = {
        'firstName': user_data['firstName'].strip(),
        'lastName': user_data['lastName'].strip(),
        'email': user_data['email'].lower().strip(),
        'age': age,
        'gender': user_data['gender'],
        'profession': user_data['profession'],
        'password': hash_password(user_data['password']),
        'created_at': datetime.now().isoformat(),
        'last_login': None
    }
    
    # Save user
    users[user_record['email']] = user_record
    save_users(users)
    
    return {'success': True, 'message': 'User registered successfully'}

def login_user(email, password):
    """Authenticate user and create session"""
    users = load_users()
    sessions = load_sessions()
    
    email = email.lower().strip()
    
    # Check if user exists
    if email not in users:
        return {'success': False, 'error': 'Invalid email or password'}
    
    user = users[email]
    
    # Verify password
    if user['password'] != hash_password(password):
        return {'success': False, 'error': 'Invalid email or password'}
    
    # Create session token
    token = generate_token()
    session_data = {
        'email': email,
        'created_at': datetime.now().isoformat(),
        'expires_at': (datetime.now() + timedelta(days=7)).isoformat()
    }
    
    # Save session
    sessions[token] = session_data
    save_sessions(sessions)
    
    # Update last login
    users[email]['last_login'] = datetime.now().isoformat()
    save_users(users)
    
    # Return user data (without password)
    user_data = {
        'name': f"{user['firstName']} {user['lastName']}",
        'firstName': user['firstName'],
        'lastName': user['lastName'],
        'email': user['email'],
        'age': user['age'],
        'gender': user['gender'],
        'profession': user['profession']
    }
    
    return {
        'success': True,
        'token': token,
        'user': user_data
    }

def verify_token(token):
    """Verify if token is valid and not expired"""
    sessions = load_sessions()
    
    if token not in sessions:
        return {'valid': False, 'error': 'Invalid token'}
    
    session = sessions[token]
    expires_at = datetime.fromisoformat(session['expires_at'])
    
    if datetime.now() > expires_at:
        # Remove expired session
        del sessions[token]
        save_sessions(sessions)
        return {'valid': False, 'error': 'Token expired'}
    
    # Get user data
    users = load_users()
    email = session['email']
    
    if email not in users:
        return {'valid': False, 'error': 'User not found'}
    
    user = users[email]
    user_data = {
        'name': f"{user['firstName']} {user['lastName']}",
        'firstName': user['firstName'],
        'lastName': user['lastName'],
        'email': user['email'],
        'age': user['age'],
        'gender': user['gender'],
        'profession': user['profession']
    }
    
    return {'valid': True, 'user': user_data}

def logout_user(token):
    """Logout user by removing session"""
    sessions = load_sessions()
    
    if token in sessions:
        del sessions[token]
        save_sessions(sessions)
        return {'success': True, 'message': 'Logged out successfully'}
    
    return {'success': False, 'error': 'Invalid token'}

def get_user_profile(email):
    """Get user profile data"""
    users = load_users()
    
    if email not in users:
        return {'success': False, 'error': 'User not found'}
    
    user = users[email]
    user_data = {
        'name': f"{user['firstName']} {user['lastName']}",
        'firstName': user['firstName'],
        'lastName': user['lastName'],
        'email': user['email'],
        'age': user['age'],
        'gender': user['gender'],
        'profession': user['profession'],
        'created_at': user['created_at'],
        'last_login': user['last_login']
    }
    
    return {'success': True, 'user': user_data}