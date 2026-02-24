"""
Configuration Management for Medical AI Skin Diagnosis System
Loads settings from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).parent.parent
BACKEND_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
FRONTEND_DIR = BASE_DIR / 'frontend'
UPLOADS_DIR = DATA_DIR / 'uploads'
LOGS_DIR = BACKEND_DIR / 'logs'


class Config:
    """Base configuration class"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5002))
    
    # Security
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    SESSION_LIFETIME_HOURS = int(os.getenv('SESSION_LIFETIME_HOURS', 24))
    PASSWORD_RESET_EXPIRY_HOURS = int(os.getenv('PASSWORD_RESET_EXPIRY_HOURS', 1))
    BCRYPT_LOG_ROUNDS = 12
    
    # AI API Keys
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # AI Configuration
    AI_REQUEST_TIMEOUT = int(os.getenv('AI_REQUEST_TIMEOUT_SECONDS', 30))
    AI_MAX_RETRIES = int(os.getenv('AI_MAX_RETRIES', 3))
    ENABLE_INTERNAL_MODELS = os.getenv('ENABLE_INTERNAL_MODELS', 'True') == 'True'
    ENABLE_EXTERNAL_APIS = os.getenv('ENABLE_EXTERNAL_APIS', 'True') == 'True'
    
    # OpenRouter Configuration
    OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'
    OPENROUTER_MODEL = 'anthropic/claude-3-haiku'
    
    # Groq Configuration
    GROQ_BASE_URL = 'https://api.groq.com/openai/v1'
    GROQ_MODEL = 'llama-3.1-70b-versatile'
    
    # Gemini Configuration
    GEMINI_MODEL = 'gemini-1.5-flash'
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@skindiagnosis.app')
    
    # File Upload
    MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE_MB', 10)) * 1024 * 1024  # Convert to bytes
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_IMAGE_EXTENSIONS', 'jpg,jpeg,png,webp').split(','))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    LOG_ROTATION_DAYS = int(os.getenv('LOG_ROTATION_DAYS', 7))
    LOG_ARCHIVE_DAYS = int(os.getenv('LOG_ARCHIVE_DAYS', 30))
    
    # Paths
    DATA_DIR = DATA_DIR
    UPLOADS_DIR = UPLOADS_DIR
    LOGS_DIR = LOGS_DIR
    
    # Data subdirectories
    USERS_DIR = DATA_DIR / 'users'
    PATIENTS_DIR = USERS_DIR / 'patients'
    DOCTORS_DIR = USERS_DIR / 'doctors'
    ADMIN_DIR = DATA_DIR / 'admin'
    DIAGNOSES_DIR = DATA_DIR / 'diagnoses'
    WALLETS_DIR = DATA_DIR / 'wallets'
    TRANSACTIONS_DIR = DATA_DIR / 'transactions'
    CONFIG_DIR = DATA_DIR / 'config'
    ASSISTANT_DIR = DATA_DIR / 'assistant'
    SESSIONS_DIR = DATA_DIR / 'sessions'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'INFO'
    BCRYPT_LOG_ROUNDS = 14


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_map.get(env, DevelopmentConfig)()
