"""
Base Configuration Module

Central control panel for Flask application configuration.
This module aggregates all configuration settings and provides
environment-specific configurations for Development and Production.

Uses Pydantic Settings for robust configuration management:
- BaseConfig: Defines everything with sensible defaults and type validation
- DevelopmentConfig: Only overrides what changes for development
- ProductionConfig: Only overrides what changes for production
"""

import os
from datetime import timedelta
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.settings.databases import DatabaseConfig
from app.settings.envcommon import BASE_DIR, Environment
from app.settings.gymconf import GymConfig


class BaseConfig(BaseSettings):
    """Base Configuration - Defines ALL settings with sensible defaults and type validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ========================================
    # Application Info
    # ========================================
    APP_NAME: str = "Gymnassic"
    APP_VERSION: str = "2.0.0"

    # ========================================
    # Gym Profile Configuration
    # ========================================
    GYM_CONFIG_PATH: str = str(BASE_DIR / "gym_profile.json")

    # ========================================
    # Flask Core Settings
    # ========================================
    DEBUG: bool = False
    TESTING: bool = False
    ENV: str = Environment.DEVELOPMENT

    # ========================================
    # Paths
    # ========================================
    BASE_DIR: Path = BASE_DIR
    INSTANCE_PATH: Path = BASE_DIR / "instance"
    TEMPLATE_FOLDER: str = "templates"
    STATIC_FOLDER: str = "static"
    STATIC_URL_PATH: str = "/static"

    # ========================================
    # Upload Configuration
    # ========================================
    UPLOAD_FOLDER: Path = BASE_DIR / "uploads"
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS: set[str] = {"png", "jpg", "jpeg", "gif", "pdf"}

    # ========================================
    # Localization
    # ========================================
    TIMEZONE: str = "UTC"

    # ========================================
    # Database Configuration
    # ========================================
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'instance' / 'gymnassic.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    # Database Engine Options
    DB_POOL_PRE_PING: bool = True
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_RECYCLE: int = 3600
    DB_POOL_TIMEOUT: int = 30
    DB_CONNECT_TIMEOUT: int = 10
    DB_APP_NAME: str = "gymnassic"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Get the database URI for SQLAlchemy."""
        return self.DATABASE_URL

    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self) -> dict:
        """Get SQLAlchemy engine options based on database type."""
        return DatabaseConfig.get_engine_options(
            database_url=self.DATABASE_URL,
            pool_size=self.DB_POOL_SIZE,
            max_overflow=self.DB_MAX_OVERFLOW,
            pool_recycle=self.DB_POOL_RECYCLE,
            pool_timeout=self.DB_POOL_TIMEOUT,
            connect_timeout=self.DB_CONNECT_TIMEOUT,
            app_name=self.DB_APP_NAME,
        )

    # ========================================
    # Security Configuration
    # ========================================
    SECRET_KEY: str = "dev-secret-key-change-in-production"

    # Session Security
    SESSION_COOKIE_SECURE: bool = False
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"
    PERMANENT_SESSION_LIFETIME: int = 3600
    REMEMBER_COOKIE_SECURE: bool = False
    PREFERRED_URL_SCHEME: str = "http"

    # CSRF Protection
    WTF_CSRF_ENABLED: bool = True
    WTF_CSRF_TIME_LIMIT: int = 3600

    # Password Policy
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_NUMBERS: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True

    # Rate Limiting
    RATELIMIT_ENABLED: bool = True
    RATELIMIT_STORAGE_URL: str = "memory://"
    RATELIMIT_DEFAULT: str = "200 per day, 50 per hour"
    RATELIMIT_LOGIN_ATTEMPTS: str = "5 per 15 minutes"

    # ========================================
    # Flask-Login Configuration
    # ========================================
    LOGIN_VIEW: str = "auth.login"
    LOGIN_MESSAGE: str = "Please log in to access this page."
    LOGIN_MESSAGE_CATEGORY: str = "info"
    REMEMBER_COOKIE_DURATION: timedelta = timedelta(days=7)

    # ========================================
    # Pagination
    # ========================================
    ITEMS_PER_PAGE: int = 20
    # ========================================
    # Email Configuration
    # ========================================
    MAIL_SERVER: str = "localhost"
    MAIL_PORT: int = 587
    MAIL_USE_TLS: bool = True
    MAIL_USE_SSL: bool = False
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_DEFAULT_SENDER: str = "noreply@gymnassic.com"
    MAIL_SUPPRESS_SEND: bool = False
    MAIL_DEBUG: bool = False
    # ========================================
    # Logging
    # ========================================
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # ========================================
    # Membership Configuration
    # ========================================
    MEMBERSHIP_GRACE_PERIOD_DAYS: int = 3
    PAYMENT_DUE_REMINDER_DAYS: int = 7

    # ========================================
    # Feature Flags
    # ========================================
    FEATURE_ONLINE_PAYMENT: bool = False
    FEATURE_EMAIL_NOTIFICATIONS: bool = True
    FEATURE_SMS_NOTIFICATIONS: bool = False

    # ========================================
    # Static Files
    # ========================================
    SEND_FILE_MAX_AGE_DEFAULT: int = 43200  # 12 hours
    EXPLAIN_TEMPLATE_LOADING: bool = False

    # ========================================
    @property
    def gym_config(self) -> GymConfig | None:
        """
        Load gym configuration from JSON file.

        Returns:
            GymConfig instance or None if file doesn't exist
        """
        try:
            return GymConfig.from_json_file(self.GYM_CONFIG_PATH)
        except FileNotFoundError:
            return None

    # ========================================
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str, info) -> str:
        """Ensure SECRET_KEY is not using default value in production."""
        if (
            info.data.get("ENV") == Environment.PRODUCTION
            and v == "dev-secret-key-change-in-production"
        ):
            raise ValueError(
                "SECRET_KEY must be set to a secure value in production. "
                "Set the SECRET_KEY environment variable."
            )
        return v

    @classmethod
    def init_app(cls, _app):
        """Initialize base configuration."""
        pass


class DevelopmentConfig(BaseConfig):
    """Development Configuration."""

    model_config = SettingsConfigDict(
        env_file=".env.development",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Environment
    ENV: str = Environment.DEVELOPMENT
    DEBUG: bool = True

    # Database: SQLite3 with echo
    SQLALCHEMY_ECHO: bool = True

    # Security: Relaxed for development
    SESSION_COOKIE_SECURE: bool = False  # Allow HTTP

    # Logging: Verbose
    LOG_LEVEL: str = "DEBUG"

    # Email: Suppress sending
    MAIL_SUPPRESS_SEND: bool = True

    # Static files: No caching
    SEND_FILE_MAX_AGE_DEFAULT: int = 0
    EXPLAIN_TEMPLATE_LOADING: bool = False

    @classmethod
    def init_app(cls, _app):
        """Initialize development-specific settings."""
        instance = cls()
        print("=" * 70)
        print(f"🏋️  {instance.APP_NAME} v{instance.APP_VERSION} - Development Mode")
        print("=" * 70)
        print(f"Environment: {instance.ENV}")
        print(f"Debug: {instance.DEBUG}")
        print(f"Database: {instance.DATABASE_URL}")
        print(f"Security: SESSION_COOKIE_SECURE = {instance.SESSION_COOKIE_SECURE}")
        print(f"Security: WTF_CSRF_ENABLED = {instance.WTF_CSRF_ENABLED}")
        print("=" * 70)


class ProductionConfig(BaseConfig):
    """Production Configuration."""

    model_config = SettingsConfigDict(
        env_file=".env.production",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Environment
    ENV: str = Environment.PRODUCTION
    DEBUG: bool = False

    # Database: PostgreSQL with connection pooling
    DATABASE_URL: str = "postgresql://localhost:5432/gymnassic_db"
    SQLALCHEMY_ECHO: bool = False

    # Security: ENFORCED (cannot be overridden)
    SECRET_KEY: str  # MANDATORY - no default
    SESSION_COOKIE_SECURE: bool = True  # Force HTTPS
    WTF_CSRF_ENABLED: bool = True  # Force CSRF protection
    REMEMBER_COOKIE_SECURE: bool = True
    PREFERRED_URL_SCHEME: str = "https"

    # Rate Limiting: Redis required for multi-worker environments
    RATELIMIT_STORAGE_URL: str = "redis://localhost:6379/0"

    # Logging: Minimal
    LOG_LEVEL: str = "WARNING"

    # Email: Enable sending
    MAIL_SUPPRESS_SEND: bool = False

    # Static files: Long cache
    SEND_FILE_MAX_AGE_DEFAULT: int = 31536000  # 1 year

    # Features: Enable online payments
    FEATURE_ONLINE_PAYMENT: bool = True

    @classmethod
    def init_app(cls, app):
        """Initialize production-specific settings."""
        import logging
        from logging.handlers import RotatingFileHandler

        instance = cls()

        # Ensure log directory exists
        log_dir = instance.BASE_DIR / "logs"
        log_dir.mkdir(exist_ok=True)

        # Set up file logging
        file_handler = RotatingFileHandler(
            log_dir / "gymnassic.log", maxBytes=10485760, backupCount=10  # 10MB
        )
        file_handler.setFormatter(logging.Formatter(instance.LOG_FORMAT))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info(f"{instance.APP_NAME} v{instance.APP_VERSION} started in PRODUCTION mode")
        app.logger.info(f"Database: PostgreSQL - {instance.DATABASE_URL}")
        app.logger.info(
            f"Security: ENFORCED - SESSION_COOKIE_SECURE = {instance.SESSION_COOKIE_SECURE}"
        )
        app.logger.info(f"Security: ENFORCED - WTF_CSRF_ENABLED = {instance.WTF_CSRF_ENABLED}")


class TestingConfig(BaseConfig):
    """Testing Configuration."""

    model_config = SettingsConfigDict(
        env_file=".env.testing",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    # Environment
    ENV: str = Environment.TESTING
    TESTING: bool = True
    DEBUG: bool = True
    # Database: In-memory SQLite for tests
    # Use in-memory database for tests
    DATABASE_URL: str = "sqlite:///:memory:"

    # Disable CSRF for testing
    WTF_CSRF_ENABLED: bool = False
    # Security: Relaxed for testing
    SESSION_COOKIE_SECURE: bool = False  # Allow HTTP
    # Disable rate limiting in tests
    RATELIMIT_ENABLED: bool = False
    # Email: Suppress sending
    MAIL_SUPPRESS_SEND: bool = True
    # Fast password hashing for tests
    PASSWORD_MIN_LENGTH: int = 4


# Configuration dictionary for easy access
config = {
    Environment.DEVELOPMENT: DevelopmentConfig,
    Environment.PRODUCTION: ProductionConfig,
    Environment.TESTING: TestingConfig,
    "default": DevelopmentConfig,
}


def get_config(env_name: str | None = None):
    if env_name is None:
        env_name = os.getenv("FLASK_ENV", Environment.DEVELOPMENT)

    config_class = config.get(env_name, config["default"])
    return config_class()
