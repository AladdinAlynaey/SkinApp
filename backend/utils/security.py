"""
Security Utilities - JWT, session management, and security helpers
"""

import jwt
import uuid
import secrets
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g
from config import get_config


config = get_config()


def generate_token(user_id: str, user_type: str, expires_hours: int = None) -> str:
    """Generate JWT access token."""
    expires = expires_hours or config.SESSION_LIFETIME_HOURS
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'exp': datetime.utcnow() + timedelta(hours=expires),
        'iat': datetime.utcnow(),
        'jti': str(uuid.uuid4())
    }
    return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm='HS256')


def verify_token(token: str) -> dict:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def generate_recovery_token() -> str:
    """Generate secure password recovery token."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """Hash a token for storage."""
    return hashlib.sha256(token.encode()).hexdigest()


def require_auth(user_types: list = None):
    """Decorator to require authentication."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing authorization token'}), 401
            
            token = auth_header.split(' ')[1]
            payload = verify_token(token)
            
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            if user_types and payload.get('user_type') not in user_types:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            g.user_id = payload.get('user_id')
            g.user_type = payload.get('user_type')
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_admin(f):
    """Decorator to require admin access."""
    return require_auth(['admin', 'super_admin'])(f)


def require_doctor(f):
    """Decorator to require doctor access."""
    return require_auth(['doctor'])(f)


def require_patient(f):
    """Decorator to require patient access."""
    return require_auth(['patient'])(f)
