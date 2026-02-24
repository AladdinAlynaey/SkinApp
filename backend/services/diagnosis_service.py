"""
Diagnosis Service - Orchestrates the AI diagnosis pipeline
"""

import time
from datetime import datetime
from storage import DiagnosisStore, UserStore
from storage.log_store import LogStore
from utils.image_utils import process_image_for_ai
from utils.logger import get_logger
from config import get_config

logger = get_logger('diagnosis_service')
config = get_config()


class DiagnosisService:
    """Orchestrates the multi-stage AI diagnosis pipeline."""
    
    def __init__(self):
        self.diagnosis_store = DiagnosisStore()
        self.user_store = UserStore()
        self.log_store = LogStore()
    
    def process(self, diagnosis_id: str):
        """Execute the full diagnosis pipeline."""
        logger.info(f"Starting diagnosis pipeline for {diagnosis_id}")
        
        diagnosis = self.diagnosis_store.get_diagnosis(diagnosis_id)
        if not diagnosis:
            logger.error(f"Diagnosis {diagnosis_id} not found")
            return False
        
        # Update status
        self.diagnosis_store.update_diagnosis(diagnosis_id, {'status': 'processing'})
        
        try:
            # Process image
            image_path = diagnosis['image']['original_path']
            processed_path, image_bytes = process_image_for_ai(image_path)
            
            # Update processed image path
            self.diagnosis_store.update_diagnosis(diagnosis_id, {
                'image': {'processed_path': processed_path}
            })
            
            # Get patient data for context
            patient = self.user_store.get_patient(diagnosis['patient_id'])
            patient_data = patient.get('profile', {}) if patient else {}
            
            # Import AI pipeline
            from ai.pipeline import DiagnosisPipeline
            pipeline = DiagnosisPipeline()
            
            # Execute pipeline
            result = pipeline.execute(
                diagnosis_id=diagnosis_id,
                image_path=processed_path,
                image_bytes=image_bytes,
                patient_data=patient_data
            )
            
            if result.get('success'):
                # Check if doctor review needed
                if diagnosis.get('doctor_review', {}).get('required'):
                    self._assign_doctor(diagnosis_id, result)
                    self.diagnosis_store.update_diagnosis(diagnosis_id, 
                        {'status': 'awaiting_review'})
                else:
                    self.diagnosis_store.update_diagnosis(diagnosis_id, 
                        {'status': 'completed'})
                
                logger.info(f"Diagnosis {diagnosis_id} completed successfully")
                return True
            else:
                self.diagnosis_store.update_diagnosis(diagnosis_id, {
                    'status': 'failed',
                    'error': result.get('error', 'Unknown error')
                })
                logger.error(f"Diagnosis {diagnosis_id} failed: {result.get('error')}")
                return False
                
        except Exception as e:
            logger.exception(f"Pipeline error for {diagnosis_id}")
            self.diagnosis_store.update_diagnosis(diagnosis_id, {
                'status': 'failed',
                'error': str(e)
            })
            self.log_store.log_error('pipeline_error', str(e), 
                                     context={'diagnosis_id': diagnosis_id})
            return False
    
    def _assign_doctor(self, diagnosis_id: str, result: dict):
        """Assign appropriate doctor based on diagnosis category."""
        from storage.json_handler import safe_read
        
        # Get category from Stage 2
        category = result.get('stage2', {}).get('category', 'general')
        
        # Find matching specialty
        specialties = safe_read(config.CONFIG_DIR / 'specialties.json', {})
        matching_specialty = None
        
        for spec in specialties.get('specialties', []):
            if category in spec.get('handles_categories', []):
                matching_specialty = spec['id']
                break
        
        # Find available doctor
        doctors = self.user_store.get_doctors_by_specialty(
            matching_specialty or 'general_dermatology'
        )
        
        if doctors:
            # Simple assignment - in production, use load balancing
            doctor = doctors[0]
            self.diagnosis_store.assign_doctor(diagnosis_id, doctor['id'])
            logger.info(f"Assigned doctor {doctor['id']} to {diagnosis_id}")


def process_diagnosis(diagnosis_id: str):
    """Entry point for diagnosis processing."""
    service = DiagnosisService()
    return service.process(diagnosis_id)
