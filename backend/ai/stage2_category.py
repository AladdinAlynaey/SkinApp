"""
Stage 2: Disease Category Classification
"""

import time
from typing import Dict
from utils.logger import get_logger

logger = get_logger('stage2')


class Stage2Category:
    """Classifies skin condition into disease category."""
    
    CATEGORIES = [
        'infectious', 'inflammatory', 'neoplastic', 
        'allergic', 'autoimmune', 'pigmentary', 'genetic'
    ]
    
    def __init__(self, router):
        self.router = router
    
    def classify(self, diagnosis_id: str, image_path: str,
                 image_bytes: bytes, stage1: Dict) -> Dict:
        """Classify into disease category."""
        start_time = time.time()
        
        data = {
            'image_path': image_path,
            'image_bytes': image_bytes,
            'diagnosis_id': diagnosis_id,
            'stage1_result': stage1,
            'categories': self.CATEGORIES
        }
        
        result = self.router.route('stage2_category', data, diagnosis_id)
        duration_ms = int((time.time() - start_time) * 1000)
        
        if result.success and result.data:
            return {
                'category': result.data.get('category', 'inflammatory'),
                'subcategory': result.data.get('subcategory'),
                'confidence': result.data.get('confidence', 0.75),
                'source': result.provider,
                'fallback_used': result.fallback_used,
                'execution_time_ms': duration_ms,
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        
        logger.warning(f"[{diagnosis_id}] Stage 2 failed, using fallback")
        return {
            'category': 'inflammatory',
            'subcategory': None,
            'confidence': 0.4,
            'source': 'fallback_default',
            'fallback_used': True,
            'execution_time_ms': duration_ms,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
