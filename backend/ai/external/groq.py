"""
Groq API Client

Fast inference for fallback and RAG operations.
"""

import requests
from typing import Dict, List
from config import get_config
from utils.logger import get_logger

logger = get_logger('groq')
config = get_config()


class GroqClient:
    """Client for Groq API."""
    
    BASE_URL = 'https://api.groq.com/openai/v1'
    
    def __init__(self):
        self.api_key = config.GROQ_API_KEY
        self.model = config.GROQ_MODEL
        self.timeout = 15  # Groq is fast
    
    def execute(self, task: str, data: Dict) -> Dict:
        """Execute AI task via Groq."""
        if not self.api_key:
            return {'success': False, 'error': 'Groq API key not configured'}
        
        prompt = self._build_prompt(task, data)
        
        try:
            response = self._call_api(prompt)
            result = self._parse_response(task, response)
            return {'success': True, 'data': result}
        except Exception as e:
            logger.error(f"Groq error: {e}")
            return {'success': False, 'error': str(e)}
    
    def chat(self, messages: List[Dict]) -> str:
        """Chat completion for assistant."""
        if not self.api_key:
            raise Exception('Groq API key not configured')
        
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
        """Make API call to Groq."""
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
        """Build prompt for task."""
        
        if task == 'stage3_diagnosis':
            return f"""You are a dermatology AI. Diagnose this condition.
Category: {data.get('category')}
Subcategory: {data.get('subcategory')}
Previous analysis: Classification was {data.get('stage1_result', {}).get('classification')}

Respond with JSON only: {{"disease": "disease_id", "confidence": 0.0-1.0, "severity": "mild/moderate/severe"}}"""
        
        elif task == 'stage4_fusion':
            return f"""Create a final diagnosis summary.
Analysis results:
- Classification: {data.get('stage1', {})}
- Category: {data.get('stage2', {})}
- Diagnosis: {data.get('stage3', {})}

Respond with JSON: {{"diagnosis": "name", "confidence": 0.0-1.0, "urgency": "routine/urgent", "recommendations": ["list"]}}"""
        
        return "Analyze this medical data."
    
    def _parse_response(self, task: str, response: str) -> Dict:
        """Parse response."""
        import json
        
        try:
            text = response.strip()
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            return json.loads(text.strip())
        except json.JSONDecodeError:
            return {'raw_response': response}
