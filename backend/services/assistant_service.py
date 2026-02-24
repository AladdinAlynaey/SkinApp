"""
AI Assistant Service - RAG-based assistant
"""

from typing import List, Dict
from storage import DiagnosisStore, UserStore
from storage.json_handler import safe_read
from utils.logger import get_logger
from config import get_config

logger = get_logger('assistant_service')
config = get_config()


class AssistantService:
    """RAG AI Assistant with context-aware responses."""
    
    def __init__(self):
        self.diagnosis_store = DiagnosisStore()
        self.user_store = UserStore()
    
    def generate(self, message: str, user_id: str, user_type: str,
                 history: List[Dict] = None) -> str:
        """Generate context-aware response."""
        
        # Build context
        context = self._build_context(user_id, user_type)
        
        # Build prompt
        system_prompt = self._build_system_prompt(user_type, context)
        
        # Try AI providers
        try:
            from ai.external.openrouter import OpenRouterClient
            client = OpenRouterClient()
            
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add history
            if history:
                for msg in history[-5:]:
                    messages.append({
                        "role": msg.get('role', 'user'),
                        "content": msg.get('content', '')
                    })
            
            messages.append({"role": "user", "content": message})
            
            response = client.chat(messages)
            return response
            
        except Exception as e:
            logger.error(f"Assistant error: {e}")
            
            # Try fallback
            try:
                from ai.external.groq import GroqClient
                client = GroqClient()
                return client.chat([
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ])
            except Exception as e2:
                logger.error(f"Fallback failed: {e2}")
                return self._fallback_response(message)
    
    def _build_context(self, user_id: str, user_type: str) -> Dict:
        """Build user context for personalization."""
        context = {"user_type": user_type}
        
        if user_type == 'patient':
            # Get patient profile and history
            patient = self.user_store.get_patient(user_id)
            if patient:
                context['profile'] = patient.get('profile', {})
            
            # Get recent diagnoses
            diagnoses = self.diagnosis_store.get_patient_history(user_id, limit=5)
            if diagnoses:
                context['recent_diagnoses'] = [
                    {
                        'date': d.get('created_at'),
                        'disease': d.get('pipeline', {}).get('stage3', {}).get('disease_name'),
                        'status': d.get('status')
                    }
                    for d in diagnoses
                ]
        
        elif user_type == 'doctor':
            doctor = self.user_store.get_doctor(user_id)
            if doctor:
                context['specialties'] = doctor.get('profile', {}).get('specialties', [])
        
        return context
    
    def _build_system_prompt(self, user_type: str, context: Dict) -> str:
        """Build system prompt based on user type."""
        
        base = """You are a medical AI assistant for a skin diagnosis application. 
You provide helpful information about skin conditions, explain diagnoses, 
and offer general guidance. Always recommend consulting a dermatologist 
for serious concerns.

IMPORTANT:
- Do NOT provide definitive diagnoses
- Always recommend professional consultation for concerning symptoms
- Be empathetic and supportive
- Answer based on verified medical information only
- If uncertain, say so clearly
"""
        
        if user_type == 'patient':
            base += """
You are speaking with a patient. Be clear, avoid jargon, and be reassuring.
Focus on education and understanding of skin conditions.
"""
            if context.get('recent_diagnoses'):
                base += f"\nPatient's recent diagnoses: {context['recent_diagnoses']}"
        
        elif user_type == 'doctor':
            base += """
You are speaking with a verified doctor. You can use medical terminology.
Focus on clinical information, research, and treatment protocols.
"""
            if context.get('specialties'):
                base += f"\nDoctor's specialties: {context['specialties']}"
        
        return base
    
    def _fallback_response(self, message: str) -> str:
        """Provide fallback response when AI fails."""
        return ("I'm currently unable to process your request due to "
                "technical difficulties. Please try again in a few moments. "
                "For urgent medical concerns, please consult a healthcare provider.")


def generate_response(message: str, user_id: str, user_type: str,
                     conversation_history: List[Dict] = None) -> str:
    """Entry point for response generation."""
    service = AssistantService()
    return service.generate(message, user_id, user_type, conversation_history)
