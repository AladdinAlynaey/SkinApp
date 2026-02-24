"""
Stage 0: Validation Gate

MANDATORY gate that validates:
1. Is the image human skin?
2. Is it a skin disease/medical image?
3. Is the image quality usable for diagnosis?

This stage MUST NEVER be skipped. If all providers fail,
the image is REJECTED with user guidance.
"""

import time
from typing import Dict
from utils.logger import get_logger

logger = get_logger('stage0')


class Stage0Gate:
    """Mandatory validation gate for diagnosis images."""
    
    def __init__(self, router):
        self.router = router
    
    def validate(self, diagnosis_id: str, image_path: str, 
                 image_bytes: bytes) -> Dict:
        """
        Validate image for diagnosis.
        
        Returns:
            Dict with is_valid, is_skin, is_medical, is_usable, rejection_reason
        """
        start_time = time.time()
        
        data = {
            'image_path': image_path,
            'image_bytes': image_bytes,
            'diagnosis_id': diagnosis_id
        }
        
        # Try routing through providers
        result = self.router.route('stage0_validation', data, diagnosis_id)
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        if result.success and result.data:
            return {
                'is_valid': True,
                'is_skin': result.data.get('is_skin', True),
                'is_medical': result.data.get('is_medical', True),
                'is_usable': result.data.get('is_usable', True),
                'confidence': result.data.get('confidence', 0.95),
                'source': result.provider,
                'fallback_used': result.fallback_used,
                'execution_time_ms': duration_ms,
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        
        # All providers failed - create rejection
        rejection_reason = self._determine_rejection_reason(result)
        
        return {
            'is_valid': False,
            'is_skin': False,
            'is_medical': False,
            'is_usable': False,
            'rejection_reason': rejection_reason,
            'user_guidance': self._get_user_guidance(rejection_reason),
            'source': 'validation_failed',
            'fallback_used': True,
            'execution_time_ms': duration_ms,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    
    def _determine_rejection_reason(self, result) -> str:
        """Determine why validation failed."""
        if result.error:
            if 'not skin' in str(result.error).lower():
                return 'not_skin_image'
            if 'quality' in str(result.error).lower():
                return 'poor_image_quality'
            if 'not medical' in str(result.error).lower():
                return 'not_medical_image'
        
        return 'validation_failed'
    
    def _get_user_guidance(self, reason: str) -> Dict:
        """Get user guidance based on rejection reason."""
        guidance = {
            'not_skin_image': {
                'en': 'Please upload a clear photo of the affected skin area.',
                'ar': 'يرجى تحميل صورة واضحة للمنطقة المصابة من الجلد.'
            },
            'poor_image_quality': {
                'en': 'The image quality is too low. Please upload a clearer, well-lit photo.',
                'ar': 'جودة الصورة منخفضة جدًا. يرجى تحميل صورة أوضح وذات إضاءة جيدة.'
            },
            'not_medical_image': {
                'en': 'This image does not appear to show a skin condition. Please upload a photo of the affected area.',
                'ar': 'لا يبدو أن هذه الصورة تظهر حالة جلدية. يرجى تحميل صورة للمنطقة المصابة.'
            },
            'validation_failed': {
                'en': 'We could not process this image. Please try again with a different photo.',
                'ar': 'لم نتمكن من معالجة هذه الصورة. يرجى المحاولة مرة أخرى بصورة مختلفة.'
            }
        }
        
        return guidance.get(reason, guidance['validation_failed'])
