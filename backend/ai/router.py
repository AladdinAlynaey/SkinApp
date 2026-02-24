"""
AI Routing with Automatic Fallback

Routes AI requests to appropriate providers with automatic failover.
"""

import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from storage.json_handler import safe_read
from storage.log_store import LogStore
from utils.logger import get_logger
from config import get_config

logger = get_logger('ai_router')
config = get_config()


@dataclass
class AIResult:
    """Result from an AI provider."""
    success: bool
    data: Optional[Dict] = None
    error: Optional[str] = None
    provider: str = ""
    duration_ms: int = 0
    fallback_used: bool = False


class AIRouter:
    """Routes AI requests with automatic failover."""
    
    def __init__(self):
        self.log_store = LogStore()
        self.config = self._load_routing_config()
        self._providers = {}
    
    def _load_routing_config(self) -> Dict:
        """Load routing configuration."""
        return safe_read(config.CONFIG_DIR / 'ai_routing.json', {
            "providers": {
                "internal": {"enabled": True, "priority": 1},
                "openrouter": {"enabled": True, "priority": 2},
                "gemini": {"enabled": True, "priority": 3},
                "groq": {"enabled": True, "priority": 4}
            },
            "fallback_behavior": {"max_retries": 3}
        })
    
    def _get_provider(self, name: str):
        """Get or create provider instance."""
        if name not in self._providers:
            if name == 'internal':
                from .internal import InternalModel
                self._providers[name] = InternalModel()
            elif name == 'openrouter':
                from .external.openrouter import OpenRouterClient
                self._providers[name] = OpenRouterClient()
            elif name == 'gemini':
                from .external.gemini import GeminiClient
                self._providers[name] = GeminiClient()
            elif name == 'groq':
                from .external.groq import GroqClient
                self._providers[name] = GroqClient()
        return self._providers.get(name)
    
    def route(self, task: str, data: Dict, diagnosis_id: str = None) -> AIResult:
        """
        Route AI request with fallback.
        
        Args:
            task: Stage name (stage0_validation, stage1_normal_abnormal, etc.)
            data: Input data for the task
            diagnosis_id: Optional diagnosis ID for logging
        """
        stage_config = self.config.get('stage_routing', {}).get(task, {})
        
        # Get provider order
        providers = stage_config.get('primary', ['internal'])
        fallbacks = stage_config.get('fallback', [])
        all_providers = providers + fallbacks
        
        fallback_used = False
        
        for idx, provider_name in enumerate(all_providers):
            # Check if provider is enabled
            provider_config = self.config.get('providers', {}).get(provider_name, {})
            if not provider_config.get('enabled', True):
                continue
            
            provider = self._get_provider(provider_name)
            if not provider:
                continue
            
            start_time = time.time()
            
            try:
                logger.debug(f"Trying {provider_name} for {task}")
                
                # Call provider
                result = provider.execute(task, data)
                
                duration_ms = int((time.time() - start_time) * 1000)
                
                if result and result.get('success'):
                    self.log_store.log_ai(
                        diagnosis_id or 'unknown', task, provider_name,
                        True, duration_ms
                    )
                    
                    return AIResult(
                        success=True,
                        data=result.get('data'),
                        provider=provider_name,
                        duration_ms=duration_ms,
                        fallback_used=fallback_used
                    )
                else:
                    raise Exception(result.get('error', 'Provider returned no result'))
                    
            except Exception as e:
                duration_ms = int((time.time() - start_time) * 1000)
                logger.warning(f"{provider_name} failed for {task}: {e}")
                
                self.log_store.log_ai(
                    diagnosis_id or 'unknown', task, provider_name,
                    False, duration_ms, str(e)
                )
                
                # Will try next provider
                fallback_used = True
                continue
        
        # All providers failed
        logger.error(f"All providers failed for {task}")
        return AIResult(
            success=False,
            error=f"All AI providers failed for {task}",
            fallback_used=True
        )
    
    def route_with_retry(self, task: str, data: Dict, 
                         max_retries: int = None) -> AIResult:
        """Route with retry logic."""
        retries = max_retries or self.config.get('fallback_behavior', {}).get('max_retries', 3)
        
        for attempt in range(retries):
            result = self.route(task, data)
            if result.success:
                return result
            
            # Exponential backoff
            if attempt < retries - 1:
                delay = (2 ** attempt) * 0.5
                time.sleep(delay)
        
        return result
