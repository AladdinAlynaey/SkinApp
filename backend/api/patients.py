"""
Patient API Endpoints
"""

from flask import Blueprint, request, jsonify, g
from storage import UserStore
from utils.security import require_patient
from utils.helpers import format_error


patients_bp = Blueprint('patients', __name__)
user_store = UserStore()


@patients_bp.route('/profile', methods=['GET'])
@require_patient
def get_profile():
    """Get patient profile."""
    patient = user_store.get_patient(g.user_id)
    if not patient:
        return jsonify(format_error("Patient not found")), 404
    return jsonify({"profile": patient})


@patients_bp.route('/profile', methods=['PUT'])
@require_patient
def update_profile():
    """Update patient profile."""
    data = request.get_json()
    
    # Fields that can be updated
    allowed_fields = ['profile', 'preferences']
    updates = {k: v for k, v in data.items() if k in allowed_fields}
    
    if not updates:
        return jsonify(format_error("No valid fields to update")), 400
    
    patient = user_store.update_patient(g.user_id, updates)
    if not patient:
        return jsonify(format_error("Patient not found")), 404
    
    return jsonify({"message": "Profile updated", "profile": patient})


@patients_bp.route('/consent', methods=['POST'])
@require_patient
def update_consent():
    """Update patient consent settings."""
    data = request.get_json()
    from utils.helpers import now_iso
    
    consent = {
        "terms_accepted": data.get('terms_accepted', False),
        "data_processing": data.get('data_processing', False),
        "ai_diagnosis": data.get('ai_diagnosis', False),
        "timestamp": now_iso()
    }
    
    patient = user_store.update_patient(g.user_id, {"consent": consent})
    return jsonify({"message": "Consent updated", "consent": consent})


@patients_bp.route('/medical-history', methods=['GET'])
@require_patient
def get_medical_history():
    """Get patient's medical history from profile."""
    patient = user_store.get_patient(g.user_id)
    if not patient:
        return jsonify(format_error("Patient not found")), 404
    
    profile = patient.get('profile', {})
    history = {
        "allergies": profile.get('allergies', []),
        "chronic_conditions": profile.get('chronic_conditions', []),
        "current_medications": profile.get('current_medications', []),
        "skin_conditions_history": profile.get('skin_conditions_history', []),
        "family_history": profile.get('family_history', [])
    }
    
    return jsonify({"medical_history": history})
