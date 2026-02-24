"""
API Blueprint Registration
"""

from flask import Flask


def register_blueprints(app: Flask):
    """Register all API blueprints."""
    from .auth import auth_bp
    from .patients import patients_bp
    from .doctors import doctors_bp
    from .admin import admin_bp
    from .diagnosis import diagnosis_bp
    from .wallet import wallet_bp
    from .assistant import assistant_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patients_bp, url_prefix='/api/patients')
    app.register_blueprint(doctors_bp, url_prefix='/api/doctors')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(diagnosis_bp, url_prefix='/api/diagnoses')
    app.register_blueprint(wallet_bp, url_prefix='/api/wallet')
    app.register_blueprint(assistant_bp, url_prefix='/api/assistant')
