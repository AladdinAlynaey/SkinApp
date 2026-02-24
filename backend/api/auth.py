"""
Authentication API Endpoints
"""

from flask import Blueprint, request, jsonify, g
from datetime import datetime, timedelta
from storage import UserStore
from storage.log_store import LogStore
from utils.validators import validate_email_address, validate_password
from utils.security import generate_token, generate_recovery_token, require_auth
from utils.helpers import get_client_ip, format_error


auth_bp = Blueprint('auth', __name__)
user_store = UserStore()
log_store = LogStore()


@auth_bp.route('/register/patient', methods=['POST'])
def register_patient():
    """Register a new patient account."""
    data = request.get_json()
    
    if not data:
        return jsonify(format_error("Request body required")), 400
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    profile = data.get('profile', {})
    
    # Validate email
    valid, error = validate_email_address(email)
    if not valid:
        return jsonify(format_error(error)), 400
    
    # Validate password
    valid, error = validate_password(password)
    if not valid:
        return jsonify(format_error(error)), 400
    
    try:
        patient = user_store.create_patient(email, password, profile)
        token = generate_token(patient['id'], 'patient')
        
        log_store.log_auth('register', patient['id'], True, get_client_ip())
        
        return jsonify({
            "message": "Registration successful",
            "user": patient,
            "token": token
        }), 201
        
    except ValueError as e:
        log_store.log_auth('register_failed', None, False, get_client_ip())
        return jsonify(format_error(str(e))), 409


@auth_bp.route('/register/doctor', methods=['POST'])
def register_doctor():
    """Register a new doctor account (pending approval)."""
    data = request.get_json()
    
    if not data:
        return jsonify(format_error("Request body required")), 400
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    profile = data.get('profile', {})
    
    # Validate required doctor fields
    if not profile.get('full_name'):
        return jsonify(format_error("Full name is required")), 400
    if not profile.get('license_number'):
        return jsonify(format_error("License number is required")), 400
    if not profile.get('specialties'):
        return jsonify(format_error("At least one specialty is required")), 400
    
    valid, error = validate_email_address(email)
    if not valid:
        return jsonify(format_error(error)), 400
    
    valid, error = validate_password(password)
    if not valid:
        return jsonify(format_error(error)), 400
    
    try:
        doctor = user_store.create_doctor(email, password, profile)
        
        log_store.log_auth('doctor_register', doctor['id'], True, get_client_ip())
        
        return jsonify({
            "message": "Registration submitted. Pending admin approval.",
            "doctor": doctor,
            "status": "pending"
        }), 201
        
    except ValueError as e:
        return jsonify(format_error(str(e))), 409


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return token."""
    data = request.get_json()
    
    if not data:
        return jsonify(format_error("Request body required")), 400
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    user_type = data.get('user_type', 'patient')
    
    if user_type not in ['patient', 'doctor', 'admin']:
        return jsonify(format_error("Invalid user type")), 400
    
    user = user_store.verify_password(email, password, user_type)
    
    if not user:
        log_store.log_auth('login_failed', None, False, get_client_ip())
        return jsonify(format_error("Invalid email or password")), 401
    
    # Check doctor approval status
    if user_type == 'doctor' and user.get('status') != 'approved':
        return jsonify(format_error(
            "Your account is pending approval",
            code="PENDING_APPROVAL"
        )), 403
    
    token = generate_token(user['id'], user_type)
    
    log_store.log_auth('login', user['id'], True, get_client_ip())
    
    return jsonify({
        "message": "Login successful",
        "user": user,
        "token": token,
        "user_type": user_type
    })


@auth_bp.route('/logout', methods=['POST'])
@require_auth()
def logout():
    """Logout current user (invalidate token)."""
    log_store.log_auth('logout', g.user_id, True, get_client_ip())
    return jsonify({"message": "Logged out successfully"})


@auth_bp.route('/recover-password', methods=['POST'])
def recover_password():
    """Send password recovery email."""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    user_type = data.get('user_type', 'patient')
    
    # Generate token regardless of whether user exists (prevent enumeration)
    token = generate_recovery_token()
    expires = (datetime.now() + timedelta(hours=1)).isoformat()
    
    # Try to set token
    success = user_store.set_recovery_token(email, user_type, token, expires)
    
    if success:
        # TODO: Send email with recovery link
        log_store.log_auth('recovery_requested', None, True, get_client_ip())
    
    # Always return success to prevent email enumeration
    return jsonify({
        "message": "If the email exists, you will receive a recovery link."
    })


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password with recovery token."""
    data = request.get_json()
    token = data.get('token', '')
    new_password = data.get('password', '')
    user_type = data.get('user_type', 'patient')
    
    valid, error = validate_password(new_password)
    if not valid:
        return jsonify(format_error(error)), 400
    
    # TODO: Find user by token and reset password
    
    return jsonify({"message": "Password reset functionality - implement token lookup"})


@auth_bp.route('/me', methods=['GET'])
@require_auth()
def get_current_user():
    """Get current authenticated user."""
    if g.user_type == 'patient':
        user = user_store.get_patient(g.user_id)
    elif g.user_type == 'doctor':
        user = user_store.get_doctor(g.user_id)
    else:
        user = {"id": g.user_id, "type": g.user_type}
    
    if not user:
        return jsonify(format_error("User not found")), 404
    
    return jsonify({"user": user, "user_type": g.user_type})
