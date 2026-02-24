"""
Google Gemini API Client

Primary vision model for image analysis.
"""

import base64
from typing import Dict, List
import google.generativeai as genai
from config import get_config
from utils.logger import get_logger

logger = get_logger('gemini')
config = get_config()


class GeminiClient:
    """Client for Google Gemini Vision API."""
    
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        self.model_name = config.GEMINI_MODEL
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None
    
    def execute(self, task: str, data: Dict) -> Dict:
        """Execute AI task via Gemini."""
        if not self.model:
            return {'success': False, 'error': 'Gemini API key not configured'}
        
        try:
            image_bytes = data.get('image_bytes')
            image_path = data.get('image_path')
            
            # Load image
            if image_bytes:
                image_data = base64.b64encode(image_bytes).decode()
            elif image_path:
                with open(image_path, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode()
            else:
                return {'success': False, 'error': 'No image provided'}
            
            prompt = self._build_prompt(task, data)
            
            # Create content with image
            image_part = {
                'mime_type': 'image/jpeg',
                'data': image_data
            }
            
            response = self.model.generate_content([prompt, image_part])
            result = self._parse_response(task, response.text)
            
            return {'success': True, 'data': result}
            
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _build_prompt(self, task: str, data: Dict) -> str:
        """Build prompt for specific task."""
        
        if task == 'stage0_validation':
            return """Analyze this image and determine:
1. Is this an image of human skin?
2. Does it show a potential skin condition or disease?
3. Is the image quality sufficient for medical analysis?

Respond ONLY with JSON:
{"is_skin": true/false, "is_medical": true/false, "is_usable": true/false, "confidence": 0.0-1.0, "reason": "explanation"}"""
        
        elif task == 'stage1_normal_abnormal':
            return """Examine this skin image and classify:
- Normal: Healthy skin with no visible abnormalities
- Abnormal: Shows signs of disease, lesion, discoloration, or inflammation

Respond ONLY with JSON: {"classification": "normal" or "abnormal", "confidence": 0.0-1.0, "observations": "what you see"}"""
        
        elif task == 'stage2_category':
            categories = data.get('categories', [])
            return f"""Classify this skin condition into one of these categories:
{categories}

Consider: lesion type, color, pattern, distribution.

Respond ONLY with JSON: {{"category": "category_id", "subcategory": "if applicable", "confidence": 0.0-1.0}}"""
        
        elif task == 'stage3_diagnosis':
            diseases = data.get('possible_diseases', [])
            disease_names = [d.get('id') for d in diseases]
            return f"""Based on visual analysis, identify the most likely condition.
Category: {data.get('category')}
Possible conditions: {disease_names}

Respond ONLY with JSON: {{"disease": "disease_id", "confidence": 0.0-1.0, "severity": "mild/moderate/severe", "key_features": ["list of observed features"]}}"""
        
        return "Analyze this medical skin image."
    
    def _parse_response(self, task: str, response: str) -> Dict:
        """Parse API response."""
        import json
        
        try:
            # Clean up response
            text = response.strip()
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            return json.loads(text.strip())
        except json.JSONDecodeError:
            logger.warning(f"Could not parse Gemini response: {response[:100]}")
            return {'raw_response': response}
