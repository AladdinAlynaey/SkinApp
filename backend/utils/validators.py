"""
Input Validation Utilities
"""

import re
from typing import Tuple, Optional
from email_validator import validate_email, EmailNotValidError


def validate_email_address(email: str) -> Tuple[bool, Optional[str]]:
    """Validate email format."""
    try:
        validate_email(email, check_deliverability=False)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain a number"
    return True, None


def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """Validate phone number format."""
    pattern = r'^\+?[1-9]\d{6,14}$'
    if re.match(pattern, phone.replace(' ', '').replace('-', '')):
        return True, None
    return False, "Invalid phone number format"


def sanitize_string(value: str, max_length: int = 500) -> str:
    """Sanitize string input."""
    if not value:
        return ""
    # Remove control characters, limit length
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', str(value))
    return sanitized[:max_length].strip()


def validate_date(date_str: str) -> Tuple[bool, Optional[str]]:
    """Validate date format (YYYY-MM-DD)."""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(pattern, date_str):
        return True, None
    return False, "Date must be in YYYY-MM-DD format"


def validate_uuid(uuid_str: str) -> bool:
    """Check if string is valid UUID."""
    pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
    return bool(re.match(pattern, uuid_str.lower()))
