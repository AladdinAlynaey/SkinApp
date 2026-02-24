"""
Stage 1: Normal vs Abnormal Classification
"""

import time
from typing import Dict
from utils.logger import get_logger

logger = get_logger('stage1')


class Stage1Classifier:
    """Classifies skin as normal or abnormal."""
    
    def __init__(self, router):
        self.router = router
    
    def classify(self, diagnosis_id: str, image_path: str,
                 image_bytes: bytes) -> Dict:
        """Classify skin as normal or abnormal."""
        start_time = time.time()
        
        data = {
            'image_path': image_path,
            'image_bytes': image_bytes,
            'diagnosis_id': diagnosis_id,
            'task': 'binary_classification',
            'classes': ['normal', 'abnormal']
        }
        
        result = self.router.route('stage1_normal_abnormal', data, diagnosis_id)
        duration_ms = int((time.time() - start_time) * 1000)
        
        if result.success and result.data:
            return {
                'classification': result.data.get('classification', 'abnormal'),
                'confidence': result.data.get('confidence', 0.85),
                'source': result.provider,
                'fallback_used': result.fallback_used,
                'execution_time_ms': duration_ms,
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        
        # Default to abnormal for safety (will be reviewed further)
        logger.warning(f"[{diagnosis_id}] Stage 1 failed, defaulting to abnormal")
        return {
            'classification': 'abnormal',
            'confidence': 0.5,
            'source': 'fallback_default',
            'fallback_used': True,
            'execution_time_ms': duration_ms,
            'note': 'Defaulted to abnormal due to AI failure',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
