"""
Logging Setup and Utilities
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from config import get_config


_loggers = {}


def setup_logging(app=None):
    """Setup application logging."""
    config = get_config()
    
    # Create log directory
    log_dir = config.LOGS_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    log_level = getattr(logging, config.LOG_LEVEL, logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # File handler
    date_str = datetime.now().strftime('%Y-%m-%d')
    file_handler = logging.FileHandler(
        log_dir / f'app_{date_str}.log',
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s'
    )
    file_handler.setFormatter(file_format)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Reduce noise from libraries
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get or create a named logger."""
    if name not in _loggers:
        _loggers[name] = logging.getLogger(name)
    return _loggers[name]
