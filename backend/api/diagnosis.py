"""
Diagnosis API Endpoints
"""

import os
from flask import Blueprint, request, jsonify, g, send_file
from werkzeug.utils import secure_filename
from storage import DiagnosisStore, WalletStore, UserStore
from storage.log_store import LogStore
from utils.security import require_auth, require_patient
from utils.image_utils import validate_image, save_uploaded_image
from utils.helpers import format_error, generate_id
from config import get_config


diagnosis_bp = Blueprint('diagnosis', __name__)
diagnosis_store = DiagnosisStore()
wallet_store = WalletStore()
user_store = UserStore()
log_store = LogStore()
config = get_config()


@diagnosis_bp.route('/upload', methods=['POST'])
@require_patient
def upload_image():
    """Upload skin image for diagnosis."""
    # Check for file
    if 'image' not in request.files:
        return jsonify(format_error("No image file provided")), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify(format_error("No file selected")), 400
    
    # Get diagnosis type
    diagnosis_type = request.form.get('type', 'ai_only')  # ai_only or ai_doctor_review
    
    # Check wallet balance
    from storage.json_handler import safe_read
    pricing = safe_read(config.CONFIG_DIR / 'pricing.json', {})
    price = pricing.get('diagnosis_prices', {}).get(diagnosis_type, {}).get('price', 10)
    
    balance = wallet_store.get_balance(g.user_id)
    if balance < price:
        return jsonify(format_error(
            f"Insufficient balance. Required: ${price}, Available: ${balance}",
            code="INSUFFICIENT_BALANCE"
        )), 402
    
    # Create diagnosis record
    diagnosis_id = generate_id()
    
    try:
        # Save image
        image_path, metadata = save_uploaded_image(file, diagnosis_id)
        
        # Validate image
        is_valid, error, _ = validate_image(image_path)
        if not is_valid:
            os.remove(image_path)
            return jsonify(format_error(error)), 400
        
        # Create diagnosis
        diagnosis = diagnosis_store.create_diagnosis(
            patient_id=g.user_id,
            image_path=image_path,
            image_metadata=metadata
        )
        
        # Update with proper ID
        diagnosis = diagnosis_store.update_diagnosis(diagnosis['id'], {
            'id': diagnosis_id,
            'doctor_review': {'required': diagnosis_type == 'ai_doctor_review'}
        })
        
        # Deduct payment
        wallet_store.debit(g.user_id, price, f"Diagnosis: {diagnosis_type}", diagnosis_id)
        
        # Start AI pipeline (async in production)
        from services.diagnosis_service import process_diagnosis
        process_diagnosis(diagnosis_id)
        
        log_store.log('api', 'diagnosis_created', {
            'diagnosis_id': diagnosis_id,
            'type': diagnosis_type,
            'price': price
        }, g.user_id)
        
        return jsonify({
            "message": "Image uploaded successfully. Processing...",
            "diagnosis_id": diagnosis_id,
            "status": "processing"
        }), 201
        
    except Exception as e:
        log_store.log_error('diagnosis_upload', str(e))
        return jsonify(format_error("Failed to process upload")), 500


@diagnosis_bp.route('/<diagnosis_id>', methods=['GET'])
@require_auth()
def get_diagnosis(diagnosis_id):
    """Get diagnosis result."""
    diagnosis = diagnosis_store.get_diagnosis(diagnosis_id)
    
    if not diagnosis:
        return jsonify(format_error("Diagnosis not found")), 404
    
    # Check authorization
    if g.user_type == 'patient' and diagnosis['patient_id'] != g.user_id:
        return jsonify(format_error("Not authorized")), 403
    
    if g.user_type == 'doctor':
        if diagnosis.get('doctor_review', {}).get('doctor_id') != g.user_id:
            return jsonify(format_error("Not authorized")), 403
    
    return jsonify({"diagnosis": diagnosis})


@diagnosis_bp.route('/history', methods=['GET'])
@require_patient
def get_history():
    """Get patient's diagnosis history."""
    limit = request.args.get('limit', 50, type=int)
    
    diagnoses = diagnosis_store.get_patient_history(g.user_id, limit=limit)
    
    return jsonify({
        "diagnoses": diagnoses,
        "total": len(diagnoses)
    })


@diagnosis_bp.route('/<diagnosis_id>/image', methods=['GET'])
@require_auth()
def get_diagnosis_image(diagnosis_id):
    """Get diagnosis image."""
    diagnosis = diagnosis_store.get_diagnosis(diagnosis_id)
    
    if not diagnosis:
        return jsonify(format_error("Diagnosis not found")), 404
    
    # Authorization check
    if g.user_type == 'patient' and diagnosis['patient_id'] != g.user_id:
        return jsonify(format_error("Not authorized")), 403
    
    image_path = diagnosis.get('image', {}).get('original_path')
    if not image_path or not os.path.exists(image_path):
        return jsonify(format_error("Image not found")), 404
    
    return send_file(image_path, mimetype='image/jpeg')


@diagnosis_bp.route('/<diagnosis_id>/status', methods=['GET'])
@require_patient
def get_status(diagnosis_id):
    """Get diagnosis processing status."""
    diagnosis = diagnosis_store.get_diagnosis(diagnosis_id)
    
    if not diagnosis:
        return jsonify(format_error("Diagnosis not found")), 404
    
    if diagnosis['patient_id'] != g.user_id:
        return jsonify(format_error("Not authorized")), 403
    
    pipeline = diagnosis.get('pipeline', {})
    stages_complete = sum(1 for s in pipeline.values() if s is not None)
    
    return jsonify({
        "status": diagnosis['status'],
        "progress": f"{stages_complete}/5",
        "stages_complete": stages_complete
    })
