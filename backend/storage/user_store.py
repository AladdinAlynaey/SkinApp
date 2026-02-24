"""
User Store - JSON-based storage for patients and doctors

Provides CRUD operations for user data with thread-safe file operations.
"""

import uuid
import bcrypt
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

from .json_handler import JSONHandler, list_json_files
from config import get_config


class UserStore:
    """
    Manages user data storage in JSON files.
    
    Directory structure:
    - data/users/patients/{user_id}.json
    - data/users/doctors/{doctor_id}.json
    - data/admin/admin.json
    """
    
    def __init__(self, config=None):
        self.config = config or get_config()
        self.patients_dir = self.config.PATIENTS_DIR
        self.doctors_dir = self.config.DOCTORS_DIR
        self.admin_path = self.config.ADMIN_DIR / 'admin.json'
    
    # ================== PATIENT OPERATIONS ==================
    
    def create_patient(self, email: str, password: str, profile: Dict = None) -> Dict:
        """
        Create a new patient account.
        
        Args:
            email: Patient email (must be unique)
            password: Plain text password (will be hashed)
            profile: Optional profile data
            
        Returns:
            Created patient data (without password hash)
            
        Raises:
            ValueError: If email already exists
        """
        # Check if email exists
        if self.get_patient_by_email(email):
            raise ValueError(f"Email {email} already registered")
        
        user_id = str(uuid.uuid4())
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        now = datetime.now().isoformat()
        
        patient_data = {
            "id": user_id,
            "email": email,
            "password_hash": password_hash,
            "created_at": now,
            "updated_at": now,
            "email_verified": False,
            "recovery_token": None,
            "recovery_expires": None,
            "profile": profile or {
                "full_name": "",
                "date_of_birth": None,
                "gender": None,
                "phone": "",
                "blood_type": None,
                "allergies": [],
                "chronic_conditions": [],
                "current_medications": [],
                "skin_type": None,
                "skin_conditions_history": [],
                "family_history": []
            },
            "preferences": {
                "language": "en",
                "theme": "light",
                "notifications": True
            },
            "consent": {
                "terms_accepted": False,
                "data_processing": False,
                "ai_diagnosis": False,
                "timestamp": None
            }
        }
        
        # Save to file
        file_path = self.patients_dir / f"{user_id}.json"
        handler = JSONHandler(file_path)
        handler.write(patient_data)
        
        # Return without password hash
        return self._sanitize_user(patient_data)
    
    def get_patient(self, user_id: str) -> Optional[Dict]:
        """Get patient by ID"""
        file_path = self.patients_dir / f"{user_id}.json"
        handler = JSONHandler(file_path)
        data = handler.read()
        return self._sanitize_user(data) if data else None
    
    def get_patient_by_email(self, email: str) -> Optional[Dict]:
        """Find patient by email"""
        for file_path in list_json_files(self.patients_dir):
            handler = JSONHandler(file_path)
            data = handler.read()
            if data and data.get('email') == email:
                return data  # Return full data for auth
        return None
    
    def update_patient(self, user_id: str, updates: Dict) -> Optional[Dict]:
        """
        Update patient data.
        
        Args:
            user_id: Patient ID
            updates: Dictionary of fields to update
            
        Returns:
            Updated patient data or None if not found
        """
        file_path = self.patients_dir / f"{user_id}.json"
        handler = JSONHandler(file_path)
        
        if not handler.exists():
            return None
        
        def apply_updates(data):
            if data is None:
                return None
            
            # Deep merge for nested objects
            for key, value in updates.items():
                if key == 'password':
                    data['password_hash'] = bcrypt.hashpw(
                        value.encode(), bcrypt.gensalt()
                    ).decode()
                elif key in data and isinstance(data[key], dict) and isinstance(value, dict):
                    data[key].update(value)
                else:
                    data[key] = value
            
            data['updated_at'] = datetime.now().isoformat()
            return data
        
        updated = handler.update(apply_updates)
        return self._sanitize_user(updated)
    
    def delete_patient(self, user_id: str) -> bool:
        """Delete patient account"""
        file_path = self.patients_dir / f"{user_id}.json"
        handler = JSONHandler(file_path)
        
        if handler.exists():
            handler.delete(backup=True)
            return True
        return False
    
    def list_patients(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """List all patients with pagination"""
        patients = []
        files = sorted(list_json_files(self.patients_dir))
        
        for file_path in files[offset:offset + limit]:
            handler = JSONHandler(file_path)
            data = handler.read()
            if data:
                patients.append(self._sanitize_user(data))
        
        return patients
    
    # ================== DOCTOR OPERATIONS ==================
    
    def create_doctor(self, email: str, password: str, profile: Dict = None) -> Dict:
        """
        Create a new doctor account (pending approval).
        
        Args:
            email: Doctor email (must be unique)
            password: Plain text password
            profile: Doctor profile with credentials
            
        Returns:
            Created doctor data
        """
        if self.get_doctor_by_email(email):
            raise ValueError(f"Email {email} already registered")
        
        doctor_id = str(uuid.uuid4())
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        now = datetime.now().isoformat()
        
        doctor_data = {
            "id": doctor_id,
            "email": email,
            "password_hash": password_hash,
            "created_at": now,
            "updated_at": now,
            "status": "pending",  # pending, approved, rejected, suspended
            "approved_by": None,
            "approved_at": None,
            "profile": profile or {
                "full_name": "",
                "photo_url": None,
                "license_number": "",
                "specialties": [],
                "qualifications": [],
                "hospital": "",
                "years_experience": 0,
                "bio": ""
            },
            "preferences": {
                "language": "en",
                "theme": "dark",
                "case_notifications": True
            },
            "statistics": {
                "cases_reviewed": 0,
                "average_rating": 0,
                "total_earnings": 0
            }
        }
        
        file_path = self.doctors_dir / f"{doctor_id}.json"
        handler = JSONHandler(file_path)
        handler.write(doctor_data)
        
        return self._sanitize_user(doctor_data)
    
    def get_doctor(self, doctor_id: str) -> Optional[Dict]:
        """Get doctor by ID"""
        file_path = self.doctors_dir / f"{doctor_id}.json"
        handler = JSONHandler(file_path)
        data = handler.read()
        return self._sanitize_user(data) if data else None
    
    def get_doctor_by_email(self, email: str) -> Optional[Dict]:
        """Find doctor by email"""
        for file_path in list_json_files(self.doctors_dir):
            handler = JSONHandler(file_path)
            data = handler.read()
            if data and data.get('email') == email:
                return data
        return None
    
    def update_doctor(self, doctor_id: str, updates: Dict) -> Optional[Dict]:
        """Update doctor data"""
        file_path = self.doctors_dir / f"{doctor_id}.json"
        handler = JSONHandler(file_path)
        
        if not handler.exists():
            return None
        
        def apply_updates(data):
            if data is None:
                return None
            
            for key, value in updates.items():
                if key == 'password':
                    data['password_hash'] = bcrypt.hashpw(
                        value.encode(), bcrypt.gensalt()
                    ).decode()
                elif key in data and isinstance(data[key], dict) and isinstance(value, dict):
                    data[key].update(value)
                else:
                    data[key] = value
            
            data['updated_at'] = datetime.now().isoformat()
            return data
        
        updated = handler.update(apply_updates)
        return self._sanitize_user(updated)
    
    def approve_doctor(self, doctor_id: str, admin_id: str) -> Optional[Dict]:
        """Approve doctor account"""
        return self.update_doctor(doctor_id, {
            'status': 'approved',
            'approved_by': admin_id,
            'approved_at': datetime.now().isoformat()
        })
    
    def reject_doctor(self, doctor_id: str, reason: str = None) -> Optional[Dict]:
        """Reject doctor application"""
        return self.update_doctor(doctor_id, {
            'status': 'rejected',
            'rejection_reason': reason
        })
    
    def list_doctors(self, status: str = None, specialty: str = None, 
                     limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        List doctors with optional filtering.
        
        Args:
            status: Filter by status (pending, approved, etc.)
            specialty: Filter by specialty
            limit: Max results
            offset: Pagination offset
            
        Returns:
            List of doctor records
        """
        doctors = []
        
        for file_path in list_json_files(self.doctors_dir):
            handler = JSONHandler(file_path)
            data = handler.read()
            
            if data:
                # Apply filters
                if status and data.get('status') != status:
                    continue
                if specialty and specialty not in data.get('profile', {}).get('specialties', []):
                    continue
                
                doctors.append(self._sanitize_user(data))
        
        # Sort by created_at descending
        doctors.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return doctors[offset:offset + limit]
    
    def get_doctors_by_specialty(self, specialty: str) -> List[Dict]:
        """Get all approved doctors with a specific specialty"""
        return self.list_doctors(status='approved', specialty=specialty)
    
    # ================== ADMIN OPERATIONS ==================
    
    def get_admin_by_email(self, email: str) -> Optional[Dict]:
        """Get admin user by email"""
        handler = JSONHandler(self.admin_path)
        data = handler.read()
        
        if data and 'users' in data:
            for admin in data['users']:
                if admin.get('email') == email:
                    return admin
        return None
    
    def verify_admin_password(self, email: str, password: str) -> Optional[Dict]:
        """Verify admin credentials"""
        admin = self.get_admin_by_email(email)
        if admin and bcrypt.checkpw(password.encode(), admin['password_hash'].encode()):
            return self._sanitize_user(admin)
        return None
    
    # ================== AUTHENTICATION HELPERS ==================
    
    def verify_password(self, email: str, password: str, user_type: str) -> Optional[Dict]:
        """
        Verify user credentials.
        
        Args:
            email: User email
            password: Plain text password
            user_type: 'patient', 'doctor', or 'admin'
            
        Returns:
            User data if valid, None otherwise
        """
        if user_type == 'patient':
            user = self.get_patient_by_email(email)
        elif user_type == 'doctor':
            user = self.get_doctor_by_email(email)
        elif user_type == 'admin':
            return self.verify_admin_password(email, password)
        else:
            return None
        
        if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            return self._sanitize_user(user)
        return None
    
    def set_recovery_token(self, email: str, user_type: str, token: str, expires: str) -> bool:
        """Set password recovery token"""
        if user_type == 'patient':
            user = self.get_patient_by_email(email)
            if user:
                self.update_patient(user['id'], {
                    'recovery_token': token,
                    'recovery_expires': expires
                })
                return True
        elif user_type == 'doctor':
            user = self.get_doctor_by_email(email)
            if user:
                self.update_doctor(user['id'], {
                    'recovery_token': token,
                    'recovery_expires': expires
                })
                return True
        return False
    
    # ================== PRIVATE HELPERS ==================
    
    def _sanitize_user(self, user: Dict) -> Dict:
        """Remove sensitive fields from user data"""
        if not user:
            return None
        
        sanitized = user.copy()
        sanitized.pop('password_hash', None)
        sanitized.pop('recovery_token', None)
        sanitized.pop('recovery_expires', None)
        return sanitized
