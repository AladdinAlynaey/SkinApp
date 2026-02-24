"""
Doctor API Endpoints
"""

from flask import Blueprint, request, jsonify, g
from storage import UserStore, DiagnosisStore
from utils.security import require_doctor
from utils.helpers import format_error


doctors_bp = Blueprint('doctors', __name__)
user_store = UserStore()
diagnosis_store = DiagnosisStore()


@doctors_bp.route('/profile', methods=['GET'])
@require_doctor
def get_profile():
    """Get doctor profile."""
    doctor = user_store.get_doctor(g.user_id)
    if not doctor:
        return jsonify(format_error("Doctor not found")), 404
    return jsonify({"profile": doctor})


@doctors_bp.route('/profile', methods=['PUT'])
@require_doctor
def update_profile():
    """Update doctor profile."""
    data = request.get_json()
    
    allowed_fields = ['profile', 'preferences']
    updates = {k: v for k, v in data.items() if k in allowed_fields}
    
    doctor = user_store.update_doctor(g.user_id, updates)
    if not doctor:
        return jsonify(format_error("Doctor not found")), 404
    
    return jsonify({"message": "Profile updated", "profile": doctor})


@doctors_bp.route('/cases', methods=['GET'])
@require_doctor
def get_assigned_cases():
    """Get cases assigned to this doctor."""
    pending_only = request.args.get('pending', 'false').lower() == 'true'
    cases = diagnosis_store.get_doctor_cases(g.user_id, pending_only=pending_only)
    
    return jsonify({
        "cases": cases,
        "total": len(cases)
    })


@doctors_bp.route('/cases/<diagnosis_id>', methods=['GET'])
@require_doctor
def get_case_detail(diagnosis_id):
    """Get detailed case information for review."""
    diagnosis = diagnosis_store.get_diagnosis(diagnosis_id)
    
    if not diagnosis:
        return jsonify(format_error("Case not found")), 404
    
    if diagnosis.get('doctor_review', {}).get('doctor_id') != g.user_id:
        return jsonify(format_error("Not authorized for this case")), 403
    
    # Include patient info (anonymized if needed)
    patient = user_store.get_patient(diagnosis['patient_id'])
    patient_info = {
        "age": None,  # Calculate from DOB
        "gender": patient.get('profile', {}).get('gender') if patient else None,
        "skin_type": patient.get('profile', {}).get('skin_type') if patient else None,
        "allergies": patient.get('profile', {}).get('allergies', []) if patient else [],
        "medical_history": patient.get('profile', {}).get('skin_conditions_history', []) if patient else []
    }
    
    return jsonify({
        "diagnosis": diagnosis,
        "patient_info": patient_info
    })


@doctors_bp.route('/cases/<diagnosis_id>/review', methods=['POST'])
@require_doctor
def submit_review(diagnosis_id):
    """Submit doctor's review of a diagnosis."""
    diagnosis = diagnosis_store.get_diagnosis(diagnosis_id)
    
    if not diagnosis:
        return jsonify(format_error("Case not found")), 404
    
    if diagnosis.get('doctor_review', {}).get('doctor_id') != g.user_id:
        return jsonify(format_error("Not authorized for this case")), 403
    
    if diagnosis.get('doctor_review', {}).get('reviewed_at'):
        return jsonify(format_error("Case already reviewed")), 400
    
    data = request.get_json()
    
    try:
        updated = diagnosis_store.submit_doctor_review(
            diagnosis_id=diagnosis_id,
            doctor_id=g.user_id,
            agrees_with_ai=data.get('agrees_with_ai', True),
            modifications=data.get('modifications'),
            notes=data.get('notes'),
            prescription=data.get('prescription')
        )
        
        # TODO: Credit doctor's wallet
        
        return jsonify({
            "message": "Review submitted successfully",
            "diagnosis": updated
        })
        
    except ValueError as e:
        return jsonify(format_error(str(e))), 400


@doctors_bp.route('/statistics', methods=['GET'])
@require_doctor
def get_statistics():
    """Get doctor's performance statistics."""
    doctor = user_store.get_doctor(g.user_id)
    
    if not doctor:
        return jsonify(format_error("Doctor not found")), 404
    
    stats = doctor.get('statistics', {
        "cases_reviewed": 0,
        "average_rating": 0,
        "total_earnings": 0
    })
    
    # Get recent cases count
    cases = diagnosis_store.get_doctor_cases(g.user_id)
    pending = [c for c in cases if not c.get('doctor_review', {}).get('reviewed_at')]
    
    stats['pending_cases'] = len(pending)
    stats['total_cases'] = len(cases)
    
    return jsonify({"statistics": stats})
