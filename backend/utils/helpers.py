"""
General Helper Functions
"""

import uuid
import json
from datetime import datetime
from typing import Any, Dict
from flask import request


def generate_id() -> str:
    """Generate a new UUID."""
    return str(uuid.uuid4())


def now_iso() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


def get_request_id() -> str:
    """Get or generate request ID."""
    return request.headers.get('X-Request-ID', generate_id())


def get_client_ip() -> str:
    """Get client IP address."""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr or 'unknown'


def safe_json_loads(data: str, default: Any = None) -> Any:
    """Safely parse JSON string."""
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def format_error(message: str, code: str = None, details: Dict = None) -> Dict:
    """Format error response."""
    error = {"error": message}
    if code:
        error["code"] = code
    if details:
        error["details"] = details
    return error


def paginate_list(items: list, page: int = 1, per_page: int = 20) -> Dict:
    """Paginate a list of items."""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        "items": items[start:end],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
    }


def localize(data: Dict, lang: str = 'en') -> str:
    """Get localized string from multilingual dict."""
    if isinstance(data, dict):
        return data.get(lang, data.get('en', str(data)))
    return str(data)
