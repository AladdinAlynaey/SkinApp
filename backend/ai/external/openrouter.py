"""
OpenRouter API Client

Primary LLM provider for text-based analysis and fusion.
"""

import requests
from typing import Dict, List
from config import get_config
from utils.logger import get_logger

logger = get_logger('openrouter')
config = get_config()


class OpenRouterClient:
    """Client for OpenRouter API."""
    
    BASE_URL = 'https://openrouter.ai/api/v1'
    
    def __init__(self):
        self.api_key = config.OPENROUTER_API_KEY
        self.model = config.OPENROUTER_MODEL
        self.timeout = config.AI_REQUEST_TIMEOUT
    
    def execute(self, task: str, data: Dict) -> Dict:
        """Execute AI task via OpenRouter."""
        if not self.api_key:
            return {'success': False, 'error': 'OpenRouter API key not configured'}
        
        prompt = self._build_prompt(task, data)
        
        try:
            response = self._call_api(prompt)
            result = self._parse_response(task, response)
            return {'success': True, 'data': result}
        except Exception as e:
            logger.error(f"OpenRouter error: {e}")
            return {'success': False, 'error': str(e)}
    
    def chat(self, messages: List[Dict]) -> str:
        """Chat completion for assistant."""
        if not self.api_key:
            raise Exception('OpenRouter API key not configured')
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': self.model,
            'messages': messages,
            'max_tokens': 1000,
            'temperature': 0.7
        }
        
        response = requests.post(
            f'{self.BASE_URL}/chat/completions',
            headers=headers,
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']
    
    def _call_api(self, prompt: str) -> str:
        """Make API call to OpenRouter."""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 500,
            'temperature': 0.3
        }
        
        response = requests.post(
            f'{self.BASE_URL}/chat/completions',
            headers=headers,
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']
    
    def _build_prompt(self, task: str, data: Dict) -> str:
        """Build prompt for specific task."""
        
        if task == 'stage1_normal_abnormal':
            return f"""Analyze this skin image description and classify as normal or abnormal.
Consider: color uniformity, texture, visible lesions, inflammation.

Context: {data.get('stage0_result', {})}

Respond ONLY with JSON: {{"classification": "normal" or "abnormal", "confidence": 0.0-1.0}}"""
        
        elif task == 'stage2_category':
            categories = data.get('categories', [])
            return f"""Based on the skin analysis, classify into one category.
Categories: {categories}

Previous analysis: {data.get('stage1_result', {})}

Respond ONLY with JSON: {{"category": "category_id", "subcategory": "subcategory_id or null", "confidence": 0.0-1.0}}"""
        
        elif task == 'stage3_diagnosis':
            diseases = [d.get('id') for d in data.get('possible_diseases', [])]
            return f"""Diagnose the skin condition from these possibilities: {diseases}
Category: {data.get('category')}

Respond ONLY with JSON: {{"disease": "disease_id", "confidence": 0.0-1.0, "severity": "mild/moderate/severe", "differential": []}}"""
        
        elif task == 'stage4_fusion':
            return f"""Generate final diagnosis report.
Stage 1: {data.get('stage1', {})}
Stage 2: {data.get('stage2', {})}
Stage 3: {data.get('stage3', {})}
Patient data: {data.get('patient_data', {})}

Respond with JSON containing: diagnosis, confidence, severity, urgency (routine/urgent/emergency), explanation, recommendations (list)."""
        
        return "Analyze this medical image."
    
    def _parse_response(self, task: str, response: str) -> Dict:
        """Parse API response into structured data."""
        import json
        
        # Try to extract JSON from response
        try:
            # Handle markdown code blocks
            if '```json' in response:
                response = response.split('```json')[1].split('```')[0]
            elif '```' in response:
                response = response.split('```')[1].split('```')[0]
            
            return json.loads(response.strip())
        except json.JSONDecodeError:
            logger.warning(f"Could not parse response as JSON: {response[:100]}")
            return {'raw_response': response}
