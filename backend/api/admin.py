"""
Admin API Endpoints
"""

from flask import Blueprint, request, jsonify, g
from storage import UserStore, DiagnosisStore
from storage.json_handler import JSONHandler, safe_read
from storage.log_store import LogStore
from utils.security import require_admin
from utils.helpers import format_error, now_iso
from config import get_config


admin_bp = Blueprint('admin', __name__)
user_store = UserStore()
diagnosis_store = DiagnosisStore()
log_store = LogStore()
config = get_config()


# ================== DOCTOR MANAGEMENT ==================

@admin_bp.route('/doctors/pending', methods=['GET'])
@require_admin
def get_pending_doctors():
    """Get doctors pending approval."""
    doctors = user_store.list_doctors(status='pending')
    return jsonify({"doctors": doctors, "total": len(doctors)})


@admin_bp.route('/doctors', methods=['GET'])
@require_admin
def list_all_doctors():
    """List all doctors."""
    status = request.args.get('status')
    doctors = user_store.list_doctors(status=status)
    return jsonify({"doctors": doctors, "total": len(doctors)})


@admin_bp.route('/doctors/<doctor_id>/approve', methods=['POST'])
@require_admin
def approve_doctor(doctor_id):
    """Approve doctor registration."""
    doctor = user_store.approve_doctor(doctor_id, g.user_id)
    if not doctor:
        return jsonify(format_error("Doctor not found")), 404
    
    log_store.log_audit('approve_doctor', g.user_id, 'doctor', doctor_id)
    return jsonify({"message": "Doctor approved", "doctor": doctor})


@admin_bp.route('/doctors/<doctor_id>/reject', methods=['POST'])
@require_admin
def reject_doctor(doctor_id):
    """Reject doctor application."""
    data = request.get_json()
    reason = data.get('reason', '')
    
    doctor = user_store.reject_doctor(doctor_id, reason)
    if not doctor:
        return jsonify(format_error("Doctor not found")), 404
    
    log_store.log_audit('reject_doctor', g.user_id, 'doctor', doctor_id)
    return jsonify({"message": "Doctor rejected", "doctor": doctor})


# ================== DISEASE MANAGEMENT ==================

@admin_bp.route('/diseases', methods=['GET'])
@require_admin
def get_diseases():
    """Get disease configuration."""
    diseases = safe_read(config.CONFIG_DIR / 'diseases.json', {})
    return jsonify(diseases)


@admin_bp.route('/diseases', methods=['PUT'])
@require_admin
def update_diseases():
    """Update disease configuration."""
    data = request.get_json()
    data['last_updated'] = now_iso()
    data['version'] = data.get('version', 0) + 1
    
    handler = JSONHandler(config.CONFIG_DIR / 'diseases.json')
    handler.write(data)
    
    log_store.log_audit('update_diseases', g.user_id, 'config', 'diseases')
    return jsonify({"message": "Diseases updated", "data": data})


# ================== SPECIALTY MANAGEMENT ==================

@admin_bp.route('/specialties', methods=['GET'])
@require_admin
def get_specialties():
    """Get specialty configuration."""
    specialties = safe_read(config.CONFIG_DIR / 'specialties.json', {})
    return jsonify(specialties)


@admin_bp.route('/specialties', methods=['PUT'])
@require_admin
def update_specialties():
    """Update specialty configuration."""
    data = request.get_json()
    data['last_updated'] = now_iso()
    
    handler = JSONHandler(config.CONFIG_DIR / 'specialties.json')
    handler.write(data)
    
    log_store.log_audit('update_specialties', g.user_id, 'config', 'specialties')
    return jsonify({"message": "Specialties updated"})


# ================== PRICING MANAGEMENT ==================

@admin_bp.route('/pricing', methods=['GET'])
@require_admin
def get_pricing():
    """Get pricing configuration."""
    pricing = safe_read(config.CONFIG_DIR / 'pricing.json', {})
    return jsonify(pricing)


@admin_bp.route('/pricing', methods=['PUT'])
@require_admin
def update_pricing():
    """Update pricing configuration."""
    data = request.get_json()
    data['last_updated'] = now_iso()
    
    handler = JSONHandler(config.CONFIG_DIR / 'pricing.json')
    handler.write(data)
    
    log_store.log_audit('update_pricing', g.user_id, 'config', 'pricing')
    return jsonify({"message": "Pricing updated"})


# ================== AI ROUTING ==================

@admin_bp.route('/ai-routing', methods=['GET'])
@require_admin
def get_ai_routing():
    """Get AI routing configuration."""
    routing = safe_read(config.CONFIG_DIR / 'ai_routing.json', {})
    return jsonify(routing)


@admin_bp.route('/ai-routing', methods=['PUT'])
@require_admin
def update_ai_routing():
    """Update AI routing configuration."""
    data = request.get_json()
    data['last_updated'] = now_iso()
    
    handler = JSONHandler(config.CONFIG_DIR / 'ai_routing.json')
    handler.write(data)
    
    log_store.log_audit('update_ai_routing', g.user_id, 'config', 'ai_routing')
    return jsonify({"message": "AI routing updated"})


# ================== LOGS ==================

@admin_bp.route('/logs/<category>', methods=['GET'])
@require_admin
def get_logs(category):
    """Get logs by category."""
    date = request.args.get('date')
    limit = request.args.get('limit', 100, type=int)
    
    if category not in ['api', 'ai', 'auth', 'errors', 'audit']:
        return jsonify(format_error("Invalid log category")), 400
    
    logs = log_store.get_logs(category, date, limit)
    return jsonify({"logs": logs, "total": len(logs)})


# ================== STATISTICS ==================

@admin_bp.route('/statistics', methods=['GET'])
@require_admin
def get_statistics():
    """Get system statistics."""
    # Patient count
    patients = user_store.list_patients(limit=10000)
    
    # Doctor counts
    doctors = user_store.list_doctors()
    pending_doctors = [d for d in doctors if d.get('status') == 'pending']
    approved_doctors = [d for d in doctors if d.get('status') == 'approved']
    
    stats = {
        "patients": {"total": len(patients)},
        "doctors": {
            "total": len(doctors),
            "pending": len(pending_doctors),
            "approved": len(approved_doctors)
        },
        "generated_at": now_iso()
    }
    
    return jsonify(stats)
