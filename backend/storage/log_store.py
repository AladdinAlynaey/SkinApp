"""
Log Store - JSON-based logging for system events
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from .json_handler import JSONHandler
from config import get_config


class LogStore:
    """Manages structured logging to JSON files."""
    
    def __init__(self, config=None):
        self.config = config or get_config()
        self.logs_dir = self.config.LOGS_DIR
    
    def _get_log_path(self, category: str) -> Path:
        """Get log file path for today."""
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_dir = self.logs_dir / category / date_str
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir / 'events.jsonl'
    
    def log(self, category: str, event_type: str, data: Dict, 
            user_id: str = None, request_id: str = None):
        """Log an event to the appropriate category file."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "request_id": request_id,
            "data": data
        }
        
        log_path = self._get_log_path(category)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False, default=str) + '\n')
    
    def log_api(self, method: str, path: str, status: int, 
                duration_ms: int, user_id: str = None, request_id: str = None):
        """Log API request."""
        self.log('api', 'request', {
            'method': method, 'path': path, 'status': status,
            'duration_ms': duration_ms
        }, user_id, request_id)
    
    def log_ai(self, diagnosis_id: str, stage: str, provider: str,
               success: bool, duration_ms: int, error: str = None):
        """Log AI pipeline execution."""
        self.log('ai', 'pipeline_stage', {
            'diagnosis_id': diagnosis_id, 'stage': stage,
            'provider': provider, 'success': success,
            'duration_ms': duration_ms, 'error': error
        })
    
    def log_auth(self, event_type: str, user_id: str, success: bool,
                 ip: str = None, user_agent: str = None):
        """Log authentication event."""
        self.log('auth', event_type, {
            'success': success, 'ip': ip, 'user_agent': user_agent
        }, user_id)
    
    def log_error(self, error_type: str, message: str, 
                  stack_trace: str = None, context: Dict = None):
        """Log error."""
        self.log('errors', error_type, {
            'message': message, 'stack_trace': stack_trace,
            'context': context or {}
        })
    
    def log_audit(self, action: str, user_id: str, resource: str,
                  resource_id: str, changes: Dict = None):
        """Log audit trail event."""
        self.log('audit', action, {
            'resource': resource, 'resource_id': resource_id,
            'changes': changes
        }, user_id)
    
    def get_logs(self, category: str, date: str = None, 
                 limit: int = 100) -> List[Dict]:
        """Read logs from a category."""
        date_str = date or datetime.now().strftime('%Y-%m-%d')
        log_path = self.logs_dir / category / date_str / 'events.jsonl'
        
        if not log_path.exists():
            return []
        
        logs = []
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    logs.append(json.loads(line))
        
        return logs[-limit:]
