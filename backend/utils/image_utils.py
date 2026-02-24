"""
Image Processing Utilities
"""

import os
import uuid
import base64
from pathlib import Path
from typing import Tuple, Optional, Dict
from PIL import Image
from config import get_config


config = get_config()


def validate_image(file_path: str) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Validate uploaded image file.
    
    Returns:
        (is_valid, error_message, metadata)
    """
    try:
        path = Path(file_path)
        
        # Check file exists
        if not path.exists():
            return False, "File not found", None
        
        # Check file size
        size = path.stat().st_size
        if size > config.MAX_UPLOAD_SIZE:
            max_mb = config.MAX_UPLOAD_SIZE / (1024 * 1024)
            return False, f"File too large. Maximum: {max_mb}MB", None
        
        # Check extension
        ext = path.suffix.lower().lstrip('.')
        if ext not in config.ALLOWED_EXTENSIONS:
            return False, f"Invalid file type. Allowed: {config.ALLOWED_EXTENSIONS}", None
        
        # Validate as image
        with Image.open(file_path) as img:
            width, height = img.size
            format_type = img.format
            mode = img.mode
        
        # Check minimum dimensions
        if width < 100 or height < 100:
            return False, "Image too small. Minimum 100x100 pixels", None
        
        metadata = {
            "size": size,
            "format": format_type,
            "dimensions": {"width": width, "height": height},
            "mode": mode
        }
        
        return True, None, metadata
        
    except Exception as e:
        return False, f"Invalid image file: {str(e)}", None


def save_uploaded_image(file_data, diagnosis_id: str) -> Tuple[str, Dict]:
    """
    Save uploaded image to diagnosis folder.
    
    Args:
        file_data: File object or bytes
        diagnosis_id: ID of the diagnosis
        
    Returns:
        (saved_path, metadata)
    """
    # Create diagnosis upload folder
    upload_dir = config.UPLOADS_DIR / 'diagnoses' / diagnosis_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    filename = f"original_{uuid.uuid4().hex[:8]}.jpg"
    save_path = upload_dir / filename
    
    # Handle different input types
    if hasattr(file_data, 'read'):
        content = file_data.read()
    elif isinstance(file_data, bytes):
        content = file_data
    elif isinstance(file_data, str) and file_data.startswith('data:'):
        # Base64 data URL
        content = base64.b64decode(file_data.split(',')[1])
    else:
        content = file_data
    
    # Save file
    with open(save_path, 'wb') as f:
        f.write(content)
    
    # Get metadata
    is_valid, _, metadata = validate_image(str(save_path))
    
    return str(save_path), metadata


def process_image_for_ai(image_path: str) -> Tuple[str, bytes]:
    """
    Process image for AI analysis.
    
    Returns:
        (processed_path, image_bytes)
    """
    with Image.open(image_path) as img:
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large (max 1024px on longest side)
        max_size = 1024
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Save processed version
        processed_dir = Path(image_path).parent
        processed_path = processed_dir / 'processed.jpg'
        img.save(processed_path, 'JPEG', quality=90)
        
        # Get bytes for API
        with open(processed_path, 'rb') as f:
            image_bytes = f.read()
    
    return str(processed_path), image_bytes


def image_to_base64(image_path: str) -> str:
    """Convert image to base64 string for API calls."""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')
