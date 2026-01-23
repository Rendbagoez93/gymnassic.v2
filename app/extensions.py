"""
Flask Extensions Registry

This module serves as a centralized registry for all Flask extension instances.
Extensions are initialized here as singletons and later bound to the Flask app
in the application factory.

NO CONFIG VALUES - Configuration is handled in app/settings/
NO APP CREATION - App is created in app/__init__.py
NO QUERIES - Database queries belong in models/repositories
NO BUSINESS LOGIC - Business logic belongs in services/views

This is ONLY a registry of service instances.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

from passlib.context import CryptContext

# ========================================
# Database Extensions
# ========================================
# Configured in: app/settings/config.py (SQLALCHEMY_*)
# SQLAlchemy ORM - Database object-relational mapper
# Used for: Database models, queries, relationships
# Configuration: SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, etc.
db = SQLAlchemy()

# Flask-Migrate - Database migration manager (Alembic wrapper)
# Used for: Creating and applying database schema migrations
# Commands: flask db init, flask db migrate, flask db upgrade
migrate = Migrate()

# ========================================
# Authentication & Authorization Extensions
# ========================================
# Configured in: app/settings/config.py (LOGIN_*, SESSION_*, PASSWORD_*)

# Flask-Login - User session management
# Used for: Login/logout, current_user, @login_required decorator
# Configuration: LOGIN_VIEW, LOGIN_MESSAGE, REMEMBER_COOKIE_DURATION
login_manager = LoginManager()


# ========================================
# Security Extensions
# ========================================
# Configured in: app/settings/config.py (WTF_CSRF_*, RATELIMIT_*, SESSION_*)

# Flask-WTF CSRF Protection
# Used for: Cross-Site Request Forgery protection on forms
# Configuration: WTF_CSRF_ENABLED, WTF_CSRF_TIME_LIMIT
csrf = CSRFProtect()

# Flask-Limiter - Rate limiting
# Used for: API rate limiting, login attempt throttling, DDoS protection
# Configuration: RATELIMIT_ENABLED, RATELIMIT_STORAGE_URL, RATELIMIT_DEFAULT
# Note: Requires Redis in production (RATELIMIT_STORAGE_URL)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],  # Set via config: RATELIMIT_DEFAULT
    storage_uri=None,   # Set via config: RATELIMIT_STORAGE_URL
)

# Flask-Talisman - HTTP security headers
# Used for: HTTPS enforcement, Content Security Policy, security headers
# Configuration: Initialized in production only via init_app
talisman = Talisman()


# ========================================
# Email Extension
# ========================================
# Configured in: app/settings/config.py (MAIL_*)

# Flask-Mail - Email sending
# Used for: Password resets, membership notifications, payment receipts
# Configuration: MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, etc.
mail = Mail()


# ========================================
# Password Hashing Utility
# ========================================
# Configured in: app/settings/config.py (PASSWORD_*)

# Passlib - Password hashing and verification
# Used for: Secure password storage, password verification
# Configuration: PASSWORD_MIN_LENGTH, PASSWORD_REQUIRE_* (validation rules only)
# Note: Uses bcrypt algorithm for secure password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Cost factor for bcrypt
)


# ========================================
# Extension Initialization Function
# ========================================

def init_extensions(app):
    """
    Initialize all Flask extensions with the application instance.
    
    This function binds all extension instances to the Flask app.
    Called from the application factory (app/__init__.py).
    
    Args:
        app: Flask application instance
        
    Extensions initialized:
        - db: SQLAlchemy (Database ORM)
        - migrate: Flask-Migrate (Database migrations)
        - login_manager: Flask-Login (Authentication)
        - csrf: CSRFProtect (CSRF protection)
        - limiter: Flask-Limiter (Rate limiting)
        - talisman: Flask-Talisman (Security headers)
        - mail: Flask-Mail (Email sending)
    
    Note:
        - pwd_context is a standalone utility and doesn't need app initialization
        - Extensions use configuration from app.config (populated from settings/)
        - Rate limiter requires Redis in production environments
    """
    
    # Database
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Authentication
    login_manager.init_app(app)
    
    # Security
    csrf.init_app(app)
    
    # Rate Limiting (only if enabled in config)
    if app.config.get('RATELIMIT_ENABLED', False):
        limiter.init_app(
            app,
            storage_uri=app.config.get('RATELIMIT_STORAGE_URL'),
            default_limits=[app.config.get('RATELIMIT_DEFAULT')],
        )
    
    # HTTPS Security Headers (production only)
    if not app.config.get('DEBUG', False):
        talisman.init_app(
            app,
            force_https=app.config.get('SESSION_COOKIE_SECURE', True),
            strict_transport_security=True,
            session_cookie_secure=app.config.get('SESSION_COOKIE_SECURE', True),
        )
    
    # Email
    mail.init_app(app)


# ========================================
# Extension Registry Export
# ========================================

__all__ = [
    # Database
    'db',
    'migrate',
    
    # Authentication
    'login_manager',
    
    # Security
    'csrf',
    'limiter',
    'talisman',
    
    # Email
    'mail',
    
    # Password
    'pwd_context',
    
    # Initialization
    'init_extensions',
]