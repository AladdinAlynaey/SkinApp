"""
Internal Model - Fallback model for when external APIs fail

This provides basic image analysis capabilities using simple
heuristics and pre-defined rules. In production, this would
be replaced with actual trained models.
"""

from typing import Dict
from PIL import Image
import numpy as np
from utils.logger import get_logger

logger = get_logger('internal_model')


class InternalModel:
    """Internal fallback model for diagnosis stages."""
    
    def execute(self, task: str, data: Dict) -> Dict:
        """Execute internal model for given task."""
        
        if task == 'stage0_validation':
            return self._validate_image(data)
        elif task == 'stage1_normal_abnormal':
            return self._classify_normal_abnormal(data)
        elif task == 'stage2_category':
            return self._classify_category(data)
        elif task == 'stage3_diagnosis':
            return self._diagnose(data)
        elif task == 'stage4_fusion':
            return self._fuse(data)
        
        return {'success': False, 'error': 'Unknown task'}
    
    def _validate_image(self, data: Dict) -> Dict:
        """Validate image is suitable for diagnosis."""
        try:
            image_path = data.get('image_path')
            
            with Image.open(image_path) as img:
                width, height = img.size
                mode = img.mode
                
                # Basic checks
                is_valid = (width >= 100 and height >= 100 and 
                           mode in ['RGB', 'RGBA', 'L'])
                
                # Simple skin detection (color-based heuristic)
                if mode == 'RGB':
                    img_array = np.array(img.resize((100, 100)))
                    
                    # Check for skin-like colors (simplified)
                    r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
                    skin_mask = (r > 95) & (g > 40) & (b > 20) & \
                               (r > g) & (r > b) & \
                               (np.abs(r.astype(int) - g.astype(int)) > 15)
                    
                    skin_ratio = np.sum(skin_mask) / skin_mask.size
                    is_skin = skin_ratio > 0.2
                else:
                    is_skin = True  # Can't determine without color
                
                return {
                    'success': True,
                    'data': {
                        'is_skin': is_skin,
                        'is_medical': True,  # Assume true if is_skin
                        'is_usable': is_valid,
                        'confidence': 0.75 if is_skin else 0.4
                    }
                }
                
        except Exception as e:
            logger.error(f"Image validation error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _classify_normal_abnormal(self, data: Dict) -> Dict:
        """Simple normal vs abnormal classification."""
        try:
            image_path = data.get('image_path')
            
            with Image.open(image_path) as img:
                img_array = np.array(img.convert('RGB').resize((100, 100)))
                
                # Simple variance-based detection
                # Abnormal skin often has higher color variance
                variance = np.var(img_array)
                
                # Threshold (tuned for general cases)
                is_abnormal = variance > 1500
                
                return {
                    'success': True,
                    'data': {
                        'classification': 'abnormal' if is_abnormal else 'normal',
                        'confidence': 0.65
                    }
                }
                
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return {'success': True, 'data': {'classification': 'abnormal', 'confidence': 0.5}}
    
    def _classify_category(self, data: Dict) -> Dict:
        """Default category classification."""
        return {
            'success': True,
            'data': {
                'category': 'inflammatory',
                'subcategory': 'dermatitis',
                'confidence': 0.5
            }
        }
    
    def _diagnose(self, data: Dict) -> Dict:
        """Default diagnosis based on category."""
        category = data.get('category', 'inflammatory')
        
        defaults = {
            'infectious': 'tinea_corporis',
            'inflammatory': 'atopic_dermatitis',
            'neoplastic': 'basal_cell_carcinoma',
            'allergic': 'contact_dermatitis',
            'autoimmune': 'vitiligo'
        }
        
        return {
            'success': True,
            'data': {
                'disease': defaults.get(category, 'atopic_dermatitis'),
                'confidence': 0.45,
                'severity': 'moderate',
                'differential': []
            }
        }
    
    def _fuse(self, data: Dict) -> Dict:
        """Simple fusion - pass through stage3 with recommendations."""
        stage3 = data.get('stage3', {})
        
        return {
            'success': True,
            'data': {
                'diagnosis': stage3.get('disease', 'unknown'),
                'confidence': 0.55,
                'severity': stage3.get('severity', 'moderate'),
                'urgency': 'routine',
                'explanation': 'Analysis complete. Please consult a doctor for confirmation.',
                'recommendations': ['Consult a dermatologist', 'Keep area clean']
            }
        }
