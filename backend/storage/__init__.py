"""
Storage module for JSON file-based persistence.
Provides thread-safe file operations with locking, versioning, and atomic writes.
"""

from .json_handler import JSONHandler, atomic_write, safe_read
from .user_store import UserStore
from .diagnosis_store import DiagnosisStore
from .wallet_store import WalletStore
from .log_store import LogStore
from .init_storage import init_storage

__all__ = [
    'JSONHandler',
    'atomic_write',
    'safe_read',
    'UserStore',
    'DiagnosisStore',
    'WalletStore',
    'LogStore',
    'init_storage'
]
