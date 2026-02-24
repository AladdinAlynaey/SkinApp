"""
Diagnosis Store - JSON-based storage for diagnosis records
"""

import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

from .json_handler import JSONHandler, list_json_files
from config import get_config


class DiagnosisStore:
    """Manages diagnosis records in JSON files."""
    
    def __init__(self, config=None):
        self.config = config or get_config()
        self.diagnoses_dir = self.config.DIAGNOSES_DIR
    
    def create_diagnosis(self, patient_id: str, image_path: str, 
                         image_metadata: Dict = None) -> Dict:
        """Create a new diagnosis record."""
        diagnosis_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        diagnosis_data = {
            "id": diagnosis_id,
            "patient_id": patient_id,
            "created_at": now,
            "updated_at": now,
            "status": "pending",
            "image": {
                "original_path": image_path,
                "processed_path": None,
                "metadata": image_metadata or {}
            },
            "pipeline": {"stage0": None, "stage1": None, "stage2": None, 
                        "stage3": None, "stage4": None},
            "doctor_review": {
                "required": False, "doctor_id": None, "assigned_at": None,
                "reviewed_at": None, "agrees_with_ai": None,
                "modifications": None, "additional_notes": None, "prescription": None
            },
            "payment": {
                "amount": 0, "currency": "USD", "status": "pending",
                "transaction_id": None, "patient_charged": 0,
                "doctor_earned": 0, "platform_fee": 0
            }
        }
        
        handler = JSONHandler(self.diagnoses_dir / f"{diagnosis_id}.json")
        handler.write(diagnosis_data)
        return diagnosis_data
    
    def get_diagnosis(self, diagnosis_id: str) -> Optional[Dict]:
        """Get diagnosis by ID"""
        handler = JSONHandler(self.diagnoses_dir / f"{diagnosis_id}.json")
        return handler.read()
    
    def update_diagnosis(self, diagnosis_id: str, updates: Dict) -> Optional[Dict]:
        """Update diagnosis record."""
        handler = JSONHandler(self.diagnoses_dir / f"{diagnosis_id}.json")
        if not handler.exists():
            return None
        
        def apply_updates(data):
            for key, value in updates.items():
                if key in data and isinstance(data[key], dict) and isinstance(value, dict):
                    data[key].update(value)
                else:
                    data[key] = value
            data['updated_at'] = datetime.now().isoformat()
            return data
        
        return handler.update(apply_updates)
    
    def update_pipeline_stage(self, diagnosis_id: str, stage: str, result: Dict) -> Optional[Dict]:
        """Update a specific pipeline stage result."""
        handler = JSONHandler(self.diagnoses_dir / f"{diagnosis_id}.json")
        
        def update_stage(data):
            if data:
                data['pipeline'][stage] = result
                data['updated_at'] = datetime.now().isoformat()
            return data
        
        return handler.update(update_stage)
    
    def assign_doctor(self, diagnosis_id: str, doctor_id: str) -> Optional[Dict]:
        """Assign a doctor for review"""
        return self.update_diagnosis(diagnosis_id, {
            'doctor_review': {'required': True, 'doctor_id': doctor_id,
                             'assigned_at': datetime.now().isoformat()}
        })
    
    def get_patient_history(self, patient_id: str, limit: int = 50) -> List[Dict]:
        """Get diagnosis history for a patient."""
        diagnoses = []
        for file_path in list_json_files(self.diagnoses_dir):
            data = JSONHandler(file_path).read()
            if data and data.get('patient_id') == patient_id:
                diagnoses.append(data)
        diagnoses.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return diagnoses[:limit]
    
    def get_doctor_cases(self, doctor_id: str, pending_only: bool = False) -> List[Dict]:
        """Get cases assigned to a doctor."""
        cases = []
        for file_path in list_json_files(self.diagnoses_dir):
            data = JSONHandler(file_path).read()
            if data and data.get('doctor_review', {}).get('doctor_id') == doctor_id:
                if pending_only and data['doctor_review'].get('reviewed_at'):
                    continue
                cases.append(data)
        return cases
