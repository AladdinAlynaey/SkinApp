"""
Stage 3: Fine-grained Disease Diagnosis
"""

import time
from typing import Dict
from storage.json_handler import safe_read
from config import get_config
from utils.logger import get_logger

logger = get_logger('stage3')
config = get_config()


class Stage3Diagnosis:
    """Provides fine-grained disease diagnosis with confidence."""
    
    def __init__(self, router):
        self.router = router
        self.diseases = self._load_diseases()
    
    def _load_diseases(self) -> Dict:
        """Load disease definitions."""
        return safe_read(config.CONFIG_DIR / 'diseases.json', {})
    
    def diagnose(self, diagnosis_id: str, image_path: str,
                 image_bytes: bytes, stage1: Dict, stage2: Dict) -> Dict:
        """Generate fine-grained diagnosis."""
        start_time = time.time()
        
        # Get diseases in this category
        category = stage2.get('category', 'inflammatory')
        category_diseases = [
            d for d in self.diseases.get('diseases', [])
            if d.get('category') == category
        ]
        
        data = {
            'image_path': image_path,
            'image_bytes': image_bytes,
            'diagnosis_id': diagnosis_id,
            'category': category,
            'subcategory': stage2.get('subcategory'),
            'possible_diseases': category_diseases,
            'stage1_result': stage1,
            'stage2_result': stage2
        }
        
        result = self.router.route('stage3_diagnosis', data, diagnosis_id)
        duration_ms = int((time.time() - start_time) * 1000)
        
        if result.success and result.data:
            disease_id = result.data.get('disease')
            disease_info = self._get_disease_info(disease_id)
            
            return {
                'disease': disease_id,
                'disease_name': disease_info.get('name', {'en': disease_id}),
                'confidence': result.data.get('confidence', 0.7),
                'severity': result.data.get('severity', 'moderate'),
                'differential_diagnoses': result.data.get('differential', []),
                'source': result.provider,
                'fallback_used': result.fallback_used,
                'execution_time_ms': duration_ms,
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        
        logger.warning(f"[{diagnosis_id}] Stage 3 failed")
        return {
            'disease': 'unknown',
            'disease_name': {'en': 'Unknown Condition', 'ar': 'حالة غير معروفة'},
            'confidence': 0.3,
            'severity': 'unknown',
            'differential_diagnoses': [],
            'source': 'fallback_default',
            'fallback_used': True,
            'requires_doctor_review': True,
            'execution_time_ms': duration_ms,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    
    def _get_disease_info(self, disease_id: str) -> Dict:
        """Get disease information from config."""
        for disease in self.diseases.get('diseases', []):
            if disease.get('id') == disease_id:
                return disease
        return {}
