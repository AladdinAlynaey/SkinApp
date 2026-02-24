"""
JSON File Handler with Thread-Safe Operations

Provides atomic writes, file locking, and safe read operations
for JSON-based data storage. Ensures data consistency even
under concurrent access.
"""

import json
import os
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional, Union
from filelock import FileLock, Timeout
from contextlib import contextmanager


class JSONHandlerError(Exception):
    """Base exception for JSON handler errors"""
    pass


class LockTimeoutError(JSONHandlerError):
    """Raised when file lock cannot be acquired"""
    pass


class FileNotFoundError(JSONHandlerError):
    """Raised when target file doesn't exist"""
    pass


class JSONHandler:
    """
    Thread-safe JSON file handler with locking and atomic writes.
    
    Features:
    - File locking to prevent race conditions
    - Atomic writes using temporary files
    - Automatic backup creation
    - Version tracking
    
    Usage:
        handler = JSONHandler(Path('/data/users/user1.json'))
        data = handler.read()
        data['name'] = 'Updated Name'
        handler.write(data)
    """
    
    DEFAULT_LOCK_TIMEOUT = 30  # seconds
    
    def __init__(self, file_path: Union[str, Path], lock_timeout: int = None):
        """
        Initialize JSON handler for a specific file.
        
        Args:
            file_path: Path to the JSON file
            lock_timeout: Maximum seconds to wait for file lock (default: 30)
        """
        self.file_path = Path(file_path)
        self.lock_path = Path(str(file_path) + '.lock')
        self.lock_timeout = lock_timeout or self.DEFAULT_LOCK_TIMEOUT
        self._lock = FileLock(self.lock_path, timeout=self.lock_timeout)
    
    @contextmanager
    def locked(self):
        """
        Context manager for file locking.
        
        Yields:
            FileLock: The acquired file lock
            
        Raises:
            LockTimeoutError: If lock cannot be acquired within timeout
        """
        try:
            with self._lock:
                yield self._lock
        except Timeout:
            raise LockTimeoutError(
                f"Could not acquire lock for {self.file_path} within {self.lock_timeout}s"
            )
    
    def read(self, default: Any = None) -> Any:
        """
        Read JSON data from file with locking.
        
        Args:
            default: Value to return if file doesn't exist (default: None)
            
        Returns:
            Parsed JSON data or default value
            
        Raises:
            LockTimeoutError: If lock cannot be acquired
            json.JSONDecodeError: If file contains invalid JSON
        """
        with self.locked():
            if not self.file_path.exists():
                return default
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    def write(self, data: Any, create_backup: bool = True) -> None:
        """
        Write JSON data to file atomically with locking.
        
        Uses temporary file + rename for atomic write operation.
        Creates backup of existing file before overwriting.
        
        Args:
            data: Data to serialize to JSON
            create_backup: Whether to backup existing file (default: True)
            
        Raises:
            LockTimeoutError: If lock cannot be acquired
        """
        with self.locked():
            # Ensure parent directory exists
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create backup if file exists
            if create_backup and self.file_path.exists():
                self._create_backup()
            
            # Write to temporary file first
            fd, temp_path = tempfile.mkstemp(
                suffix='.json',
                prefix='.tmp_',
                dir=self.file_path.parent
            )
            
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2, default=str)
                
                # Atomic rename (works on both Windows and Unix)
                if os.name == 'nt':  # Windows
                    if self.file_path.exists():
                        os.remove(self.file_path)
                    os.rename(temp_path, self.file_path)
                else:  # Unix
                    os.rename(temp_path, self.file_path)
                    
            except Exception as e:
                # Clean up temp file on error
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise e
    
    def update(self, update_fn: callable, create_backup: bool = True) -> Any:
        """
        Read, modify, and write data in a single locked transaction.
        
        Args:
            update_fn: Function that takes current data and returns modified data
            create_backup: Whether to backup before writing (default: True)
            
        Returns:
            The updated data
            
        Example:
            def add_item(data):
                data['items'].append({'id': 'new'})
                return data
            handler.update(add_item)
        """
        with self.locked():
            data = None
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            # Apply update function
            updated_data = update_fn(data)
            
            # Write updated data (without re-acquiring lock)
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if create_backup and self.file_path.exists():
                self._create_backup()
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=2, default=str)
            
            return updated_data
    
    def _create_backup(self) -> None:
        """Create timestamped backup of current file"""
        if not self.file_path.exists():
            return
        
        backup_dir = self.file_path.parent / '.backups'
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{self.file_path.stem}_{timestamp}{self.file_path.suffix}"
        backup_path = backup_dir / backup_name
        
        shutil.copy2(self.file_path, backup_path)
        
        # Keep only last 10 backups
        backups = sorted(backup_dir.glob(f"{self.file_path.stem}_*{self.file_path.suffix}"))
        if len(backups) > 10:
            for old_backup in backups[:-10]:
                old_backup.unlink()
    
    def exists(self) -> bool:
        """Check if the JSON file exists"""
        return self.file_path.exists()
    
    def delete(self, backup: bool = True) -> None:
        """
        Delete the JSON file.
        
        Args:
            backup: Whether to create backup before deletion (default: True)
        """
        with self.locked():
            if self.file_path.exists():
                if backup:
                    self._create_backup()
                self.file_path.unlink()
            
            # Also remove lock file
            if self.lock_path.exists():
                self.lock_path.unlink()


def atomic_write(file_path: Union[str, Path], data: Any) -> None:
    """
    Convenience function for one-off atomic writes.
    
    Args:
        file_path: Path to JSON file
        data: Data to write
    """
    handler = JSONHandler(file_path)
    handler.write(data)


def safe_read(file_path: Union[str, Path], default: Any = None) -> Any:
    """
    Convenience function for safe reads with locking.
    
    Args:
        file_path: Path to JSON file
        default: Value to return if file doesn't exist
        
    Returns:
        Parsed JSON data or default
    """
    handler = JSONHandler(file_path)
    return handler.read(default)


def list_json_files(directory: Union[str, Path], pattern: str = "*.json") -> list:
    """
    List all JSON files in a directory.
    
    Args:
        directory: Directory path to search
        pattern: Glob pattern to match (default: *.json)
        
    Returns:
        List of Path objects for matching files
    """
    path = Path(directory)
    if not path.exists():
        return []
    return list(path.glob(pattern))


def merge_json_data(target: Dict, source: Dict, deep: bool = True) -> Dict:
    """
    Merge two JSON-compatible dictionaries.
    
    Args:
        target: Base dictionary
        source: Dictionary to merge into target
        deep: If True, recursively merge nested dicts (default: True)
        
    Returns:
        Merged dictionary
    """
    result = target.copy()
    
    for key, value in source.items():
        if deep and key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_json_data(result[key], value, deep=True)
        else:
            result[key] = value
    
    return result
