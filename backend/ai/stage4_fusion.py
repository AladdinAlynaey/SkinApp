"""
Stage 4: AI Fusion Layer

Combines all AI outputs with patient data to produce
final diagnosis with explanations and recommendations.
"""

import time
from typing import Dict
from utils.logger import get_logger

logger = get_logger('stage4')


class Stage4Fusion:
    """Fusion layer combining all AI outputs."""
    
    def __init__(self, router):
        self.router = router
    
    def fuse(self, diagnosis_id: str, patient_data: Dict,
             stage1: Dict, stage2: Dict, stage3: Dict) -> Dict:
        """Fuse all data into final diagnosis."""
        start_time = time.time()
        
        # Check if normal
        if stage1.get('classification') == 'normal':
            return self._normal_result(diagnosis_id, start_time)
        
        # Gather context
        data = {
            'diagnosis_id': diagnosis_id,
            'patient_data': patient_data,
            'stage1': stage1,
            'stage2': stage2,
            'stage3': stage3
        }
        
        result = self.router.route('stage4_fusion', data, diagnosis_id)
        duration_ms = int((time.time() - start_time) * 1000)
        
        if result.success and result.data:
            return {
                'final_diagnosis': result.data.get('diagnosis', stage3.get('disease')),
                'final_confidence': self._calculate_confidence(stage1, stage2, stage3, result.data),
                'severity': result.data.get('severity', stage3.get('severity', 'moderate')),
                'urgency': result.data.get('urgency', 'routine'),
                'explanation': result.data.get('explanation', ''),
                'recommendations': result.data.get('recommendations', []),
                'follow_up': result.data.get('follow_up', 'consult_doctor'),
                'sources_used': ['stage1', 'stage2', 'stage3', 'patient_history'],
                'source': result.provider,
                'fallback_used': result.fallback_used,
                'execution_time_ms': duration_ms,
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        
        # Fallback: use stage3 result directly
        return self._fallback_result(stage3, patient_data, duration_ms)
    
    def _normal_result(self, diagnosis_id: str, start_time: float) -> Dict:
        """Result for normal skin classification."""
        duration_ms = int((time.time() - start_time) * 1000)
        
        return {
            'final_diagnosis': 'normal_skin',
            'final_confidence': 0.9,
            'severity': 'none',
            'urgency': 'none',
            'explanation': {
                'en': 'The skin appears healthy with no visible abnormalities.',
                'ar': 'يبدو الجلد صحيًا بدون أي تشوهات مرئية.'
            },
            'recommendations': [
                {'en': 'Continue regular skincare routine', 'ar': 'استمر في روتين العناية بالبشرة'},
                {'en': 'Use sunscreen daily', 'ar': 'استخدم واقي الشمس يوميًا'},
                {'en': 'Monitor for any changes', 'ar': 'راقب أي تغييرات'}
            ],
            'follow_up': 'none',
            'sources_used': ['stage1'],
            'execution_time_ms': duration_ms,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    
    def _fallback_result(self, stage3: Dict, patient_data: Dict, 
                          duration_ms: int) -> Dict:
        """Generate fallback result from stage3."""
        disease = stage3.get('disease', 'unknown')
        
        return {
            'final_diagnosis': disease,
            'final_confidence': stage3.get('confidence', 0.5) * 0.8,
            'severity': stage3.get('severity', 'moderate'),
            'urgency': 'consult_doctor',
            'explanation': {
                'en': 'AI analysis indicates a potential skin condition. Please consult a dermatologist.',
                'ar': 'يشير تحليل الذكاء الاصطناعي إلى حالة جلدية محتملة. يرجى استشارة طبيب جلدية.'
            },
            'recommendations': [
                {'en': 'Consult a dermatologist', 'ar': 'استشر طبيب جلدية'},
                {'en': 'Keep the area clean and dry', 'ar': 'حافظ على المنطقة نظيفة وجافة'},
                {'en': 'Avoid scratching', 'ar': 'تجنب الحك'}
            ],
            'follow_up': '1_week',
            'sources_used': ['stage3'],
            'source': 'fallback_fusion',
            'fallback_used': True,
            'execution_time_ms': duration_ms,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    
    def _calculate_confidence(self, stage1: Dict, stage2: Dict, 
                               stage3: Dict, fusion: Dict) -> float:
        """Calculate weighted confidence score."""
        weights = {'stage1': 0.1, 'stage2': 0.2, 'stage3': 0.4, 'fusion': 0.3}
        
        total = (
            stage1.get('confidence', 0.8) * weights['stage1'] +
            stage2.get('confidence', 0.7) * weights['stage2'] +
            stage3.get('confidence', 0.6) * weights['stage3'] +
            fusion.get('confidence', 0.7) * weights['fusion']
        )
        
        return round(min(total, 0.99), 2)
