"""
Authentication Service
"""

from datetime import datetime, timedelta
from storage import UserStore
from utils.security import generate_token, generate_recovery_token, hash_token


class AuthService:
    """Handles authentication business logic."""
    
    def __init__(self):
        self.user_store = UserStore()
    
    def authenticate(self, email: str, password: str, user_type: str):
        """Authenticate user and return token."""
        user = self.user_store.verify_password(email, password, user_type)
        if not user:
            return None, "Invalid credentials"
        
        if user_type == 'doctor' and user.get('status') != 'approved':
            return None, "Account pending approval"
        
        token = generate_token(user['id'], user_type)
        return {"user": user, "token": token}, None
    
    def request_password_reset(self, email: str, user_type: str):
        """Generate password reset token."""
        token = generate_recovery_token()
        expires = (datetime.now() + timedelta(hours=1)).isoformat()
        
        success = self.user_store.set_recovery_token(email, user_type, 
                                                      hash_token(token), expires)
        if success:
            # Return plain token for email
            return token
        return None
