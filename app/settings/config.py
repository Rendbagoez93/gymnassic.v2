"""
Base Configuration Module

Central control panel for Flask application configuration.
This module aggregates all configuration settings and provides
environment-specific configurations for Development and Production.

Uses composition-style override pattern:
- BaseConfig: Defines everything with sensible defaults
- DevelopmentConfig: Only overrides what changes for development
- ProductionConfig: Only overrides what changes for production
"""

import os
from datetime import timedelta
from .envcommon import Environment, get_env, get_bool_env, get_int_env, BASE_DIR


class BaseConfig:
    # Base Configuration - Defines ALL settings with sensible defaults.
    # ========================================
    # Application Info
    # ========================================
    APP_NAME = "Gymnassic"
    APP_VERSION = "2.0.0"
    
    # ========================================
    # Flask Core Settings
    # ========================================
    DEBUG = False
    TESTING = False
    ENV = Environment.DEVELOPMENT
    
    # ========================================
    # Paths
    # ========================================
    BASE_DIR = BASE_DIR
    INSTANCE_PATH = BASE_DIR / "instance"
    TEMPLATE_FOLDER = "templates"
    STATIC_FOLDER = "static"
    STATIC_URL_PATH = "/static"
    
    # ========================================
    # Upload Configuration
    # ========================================
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    MAX_CONTENT_LENGTH = get_int_env("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)  # 16MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}
    
    # ========================================
    # Localization
    # ========================================
    TIMEZONE = get_env("TIMEZONE", "UTC")
    
    # ========================================
    # Database Configuration (SQLite3 Default)
    # ========================================
    SQLALCHEMY_DATABASE_URI = get_env(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'instance' / 'gymnassic.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = get_bool_env("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    SQLALCHEMY_ECHO = get_bool_env("SQLALCHEMY_ECHO", False)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": get_bool_env("DB_POOL_PRE_PING", True),
        "connect_args": {
            "check_same_thread": False,  # SQLite: allow multi-threading
        },
    }
    
    # ========================================
    # Security Configuration
    # ========================================
    SECRET_KEY = get_env("SECRET_KEY", default="dev-secret-key-change-in-production")
    
    # Session Security
    SESSION_COOKIE_SECURE = get_bool_env("SESSION_COOKIE_SECURE", False)
    SESSION_COOKIE_HTTPONLY = get_bool_env("SESSION_COOKIE_HTTPONLY", True)
    SESSION_COOKIE_SAMESITE = get_env("SESSION_COOKIE_SAMESITE", "Lax")
    PERMANENT_SESSION_LIFETIME = get_int_env("PERMANENT_SESSION_LIFETIME", 3600)
    
    # CSRF Protection
    WTF_CSRF_ENABLED = get_bool_env("WTF_CSRF_ENABLED", True)
    WTF_CSRF_TIME_LIMIT = get_int_env("WTF_CSRF_TIME_LIMIT", 3600)
    
    # Password Policy (values only)
    PASSWORD_MIN_LENGTH = get_int_env("PASSWORD_MIN_LENGTH", 8)
    PASSWORD_REQUIRE_UPPERCASE = get_bool_env("PASSWORD_REQUIRE_UPPERCASE", True)
    PASSWORD_REQUIRE_LOWERCASE = get_bool_env("PASSWORD_REQUIRE_LOWERCASE", True)
    PASSWORD_REQUIRE_NUMBERS = get_bool_env("PASSWORD_REQUIRE_NUMBERS", True)
    PASSWORD_REQUIRE_SPECIAL = get_bool_env("PASSWORD_REQUIRE_SPECIAL", True)
    
    # Rate Limiting
    RATELIMIT_ENABLED = get_bool_env("RATELIMIT_ENABLED", True)
    RATELIMIT_STORAGE_URL = get_env("RATELIMIT_STORAGE_URL", "memory://")
    RATELIMIT_DEFAULT = get_env("RATELIMIT_DEFAULT", "200 per day, 50 per hour")
    RATELIMIT_LOGIN_ATTEMPTS = get_env("RATELIMIT_LOGIN_ATTEMPTS", "5 per 15 minutes")
    
    # ========================================
    # Flask-Login Configuration
    # ========================================
    LOGIN_VIEW = "auth.login"
    LOGIN_MESSAGE = "Please log in to access this page."
    LOGIN_MESSAGE_CATEGORY = "info"
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    
    # ========================================
    # Pagination
    # ========================================
    ITEMS_PER_PAGE = get_int_env("ITEMS_PER_PAGE", 20)
    
    # ========================================
    # Email Configuration
    # ========================================
    MAIL_SERVER = get_env("MAIL_SERVER", "localhost")
    MAIL_PORT = get_int_env("MAIL_PORT", 587)
    MAIL_USE_TLS = get_bool_env("MAIL_USE_TLS", True)
    MAIL_USE_SSL = get_bool_env("MAIL_USE_SSL", False)
    MAIL_USERNAME = get_env("MAIL_USERNAME")
    MAIL_PASSWORD = get_env("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = get_env("MAIL_DEFAULT_SENDER", "noreply@gymnassic.com")
    MAIL_SUPPRESS_SEND = get_bool_env("MAIL_SUPPRESS_SEND", False)
    
    # ========================================
    # Logging
    # ========================================
    LOG_LEVEL = get_env("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # ========================================
    # Membership Configuration
    # ========================================
    MEMBERSHIP_GRACE_PERIOD_DAYS = get_int_env("MEMBERSHIP_GRACE_PERIOD_DAYS", 3)
    PAYMENT_DUE_REMINDER_DAYS = get_int_env("PAYMENT_DUE_REMINDER_DAYS", 7)
    
    # ========================================
    # Feature Flags
    # ========================================
    FEATURE_ONLINE_PAYMENT = get_bool_env("FEATURE_ONLINE_PAYMENT", False)
    FEATURE_EMAIL_NOTIFICATIONS = get_bool_env("FEATURE_EMAIL_NOTIFICATIONS", True)
    FEATURE_SMS_NOTIFICATIONS = get_bool_env("FEATURE_SMS_NOTIFICATIONS", False)
    
    # ========================================
    # Static Files
    # ========================================
    SEND_FILE_MAX_AGE_DEFAULT = 43200  # 12 hours


class DevelopmentConfig(BaseConfig):
    # Development Configuration. 
    # Environment
    ENV = Environment.DEVELOPMENT
    DEBUG = True
    
    # Database: SQLite3 with echo
    SQLALCHEMY_DATABASE_URI = get_env(
        "DATABASE_URL",
        default=f"sqlite:///{BaseConfig.BASE_DIR / 'instance' / 'gymnassic.db'}"
    )
    SQLALCHEMY_ECHO = get_bool_env("SQLALCHEMY_ECHO", True)
    
    # Security: Relaxed for development
    SESSION_COOKIE_SECURE = False  # Allow HTTP
    
    # Logging: Verbose
    LOG_LEVEL = get_env("LOG_LEVEL", "DEBUG")
    
    # Email: Suppress sending
    MAIL_SUPPRESS_SEND = get_bool_env("MAIL_SUPPRESS_SEND", True)
    
    # Static files: No caching
    SEND_FILE_MAX_AGE_DEFAULT = 0
    EXPLAIN_TEMPLATE_LOADING = get_bool_env("EXPLAIN_TEMPLATE_LOADING", False)
    
    @classmethod
    def init_app(cls, app):
        """Initialize development-specific settings"""
        print("=" * 70)
        print(f"🏋️  {cls.APP_NAME} v{cls.APP_VERSION} - Development Mode")
        print("=" * 70)
        print(f"Environment: {cls.ENV}")
        print(f"Debug: {cls.DEBUG}")
        print(f"Database: SQLite3 - {cls.SQLALCHEMY_DATABASE_URI}")
        print(f"Security: SESSION_COOKIE_SECURE = {cls.SESSION_COOKIE_SECURE}")
        print(f"Security: WTF_CSRF_ENABLED = {cls.WTF_CSRF_ENABLED}")
        print("=" * 70)


class ProductionConfig(BaseConfig):
    # Production Configuration.
    # Environment
    ENV = Environment.PRODUCTION
    DEBUG = False
    
    # Database: PostgreSQL with connection pooling
    SQLALCHEMY_DATABASE_URI = get_env(
        "DATABASE_URL",
        default="postgresql://localhost:5432/gymnassic_db"
    )
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": get_int_env("DB_POOL_SIZE", 10),
        "max_overflow": get_int_env("DB_MAX_OVERFLOW", 20),
        "pool_recycle": get_int_env("DB_POOL_RECYCLE", 3600),
        "pool_pre_ping": get_bool_env("DB_POOL_PRE_PING", True),
        "pool_timeout": get_int_env("DB_POOL_TIMEOUT", 30),
        "connect_args": {
            "connect_timeout": get_int_env("DB_CONNECT_TIMEOUT", 10),
            "application_name": get_env("DB_APP_NAME", "gymnassic"),
        },
    }
    
    # Security: ENFORCED (cannot be overridden)
    SECRET_KEY = get_env("SECRET_KEY", required=True)  # MANDATORY
    SESSION_COOKIE_SECURE = True  # Force HTTPS
    WTF_CSRF_ENABLED = True  # Force CSRF protection
    REMEMBER_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = "https"
    
    # Rate Limiting: Redis required for multi-worker environments
    RATELIMIT_STORAGE_URL = get_env("RATELIMIT_STORAGE_URL", default="redis://localhost:6379/0")
    
    # Logging: Minimal
    LOG_LEVEL = get_env("LOG_LEVEL", "WARNING")
    
    # Email: Enable sending
    MAIL_SUPPRESS_SEND = False
    
    # Static files: Long cache
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year
    
    # Features: Enable online payments
    FEATURE_ONLINE_PAYMENT = get_bool_env("FEATURE_ONLINE_PAYMENT", True)
    
    @classmethod
    def init_app(cls, app):
        """Initialize production-specific settings"""
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Ensure log directory exists
        log_dir = cls.BASE_DIR / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # Set up file logging
        file_handler = RotatingFileHandler(
            log_dir / "gymnassic.log",
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info(f"{cls.APP_NAME} v{cls.APP_VERSION} started in PRODUCTION mode")
        app.logger.info(f"Database: PostgreSQL - {cls.SQLALCHEMY_DATABASE_URI}")
        app.logger.info(f"Security: ENFORCED - SESSION_COOKIE_SECURE = {cls.SESSION_COOKIE_SECURE}")
        app.logger.info(f"Security: ENFORCED - WTF_CSRF_ENABLED = {cls.WTF_CSRF_ENABLED}")


class TestingConfig(BaseConfig):
    ENV = Environment.TESTING
    TESTING = True
    DEBUG = True
    
    # Use in-memory database for tests
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Disable rate limiting in tests
    RATELIMIT_ENABLED = False
    
    # Fast password hashing for tests
    PASSWORD_MIN_LENGTH = 4


# Configuration dictionary for easy access
config = {
    Environment.DEVELOPMENT: DevelopmentConfig,
    Environment.PRODUCTION: ProductionConfig,
    Environment.TESTING: TestingConfig,
    "default": DevelopmentConfig,
}


def get_config(env_name: str = None):
    if env_name is None:
        env_name = os.getenv("FLASK_ENV", Environment.DEVELOPMENT)
    
    return config.get(env_name, config["default"])

