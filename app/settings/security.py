"""
Security Configuration Module

Manages security-related settings including secret keys, session configuration,
CSRF protection, and rate limiting.

This module provides base security settings and environment-specific overrides
for Development and Production environments.
"""

from .envcommon import get_env, get_bool_env, get_int_env


class SecurityConfig:
    # Secret Key - Used for session signing, CSRF tokens, etc.
    # Development: Uses a default key (not secure, but convenient)
    # Production: MUST be set via environment variable (enforced in ProductionSecurityConfig)
    SECRET_KEY = get_env(
        "SECRET_KEY",
        default="dev-secret-key-change-in-production"
    )
    
    # ========================================
    # Session Configuration
    # ========================================
    
    # Secure cookies (HTTPS only)
    # Development: False (allows HTTP for local testing)
    # Production: True (enforced in ProductionSecurityConfig)
    SESSION_COOKIE_SECURE = get_bool_env("SESSION_COOKIE_SECURE", False)
    
    # HTTP-only cookies (prevents JavaScript access)
    SESSION_COOKIE_HTTPONLY = get_bool_env("SESSION_COOKIE_HTTPONLY", True)
    
    # SameSite cookie policy
    SESSION_COOKIE_SAMESITE = get_env("SESSION_COOKIE_SAMESITE", "Lax")
    
    # Session lifetime in seconds (default: 1 hour)
    PERMANENT_SESSION_LIFETIME = get_int_env("PERMANENT_SESSION_LIFETIME", 3600)
    
    # ========================================
    # CSRF Protection
    # ========================================
    
    # Enable CSRF protection
    # Development: Can be toggled via env var
    # Production: True (enforced in ProductionSecurityConfig)
    WTF_CSRF_ENABLED = get_bool_env("WTF_CSRF_ENABLED", True)
    
    # CSRF token time limit in seconds (default: 1 hour)
    WTF_CSRF_TIME_LIMIT = get_int_env("WTF_CSRF_TIME_LIMIT", 3600)
    
    # ========================================
    # Password Policy (Values Only - No Logic)
    # ========================================
    # These are configuration values only.
    # Password validation logic should be implemented in your auth module.
    
    PASSWORD_MIN_LENGTH = get_int_env("PASSWORD_MIN_LENGTH", 8)
    PASSWORD_REQUIRE_UPPERCASE = get_bool_env("PASSWORD_REQUIRE_UPPERCASE", True)
    PASSWORD_REQUIRE_LOWERCASE = get_bool_env("PASSWORD_REQUIRE_LOWERCASE", True)
    PASSWORD_REQUIRE_NUMBERS = get_bool_env("PASSWORD_REQUIRE_NUMBERS", True)
    PASSWORD_REQUIRE_SPECIAL = get_bool_env("PASSWORD_REQUIRE_SPECIAL", True)
    
    # ========================================
    # Rate Limiting
    # ========================================
    # NOTE: For production, Redis is REQUIRED for rate limiting to work
    # across multiple processes/workers.
    #
    # Development: Uses memory:// (single process only)
    # Production: Should use redis://localhost:6379/0 or similar
    #
    # Install Redis: https://redis.io/download
    # Connection format: redis://host:port/db or redis://user:password@host:port/db
    
    RATELIMIT_ENABLED = get_bool_env("RATELIMIT_ENABLED", True)
    
    # Storage backend for rate limiting
    # Development: memory:// (not shared across processes)
    # Production: redis://localhost:6379/0 (shared, persistent)
    RATELIMIT_STORAGE_URL = get_env("RATELIMIT_STORAGE_URL", "memory://")
    
    # Default rate limits
    RATELIMIT_DEFAULT = get_env("RATELIMIT_DEFAULT", "200 per day, 50 per hour")
    
    # Login-specific rate limiting (prevents brute force attacks)
    RATELIMIT_LOGIN_ATTEMPTS = get_env("RATELIMIT_LOGIN_ATTEMPTS", "5 per 15 minutes")


class DevelopmentSecurityConfig(SecurityConfig):
    # Allow non-secure cookies for HTTP during development
    SESSION_COOKIE_SECURE = False
    
    # Use memory-based rate limiting (no Redis required)
    RATELIMIT_STORAGE_URL = get_env("RATELIMIT_STORAGE_URL", "memory://")


class ProductionSecurityConfig(SecurityConfig):
    # ========================================
    # ENFORCED PRODUCTION SECURITY
    # ========================================
    
    # SECRET_KEY is REQUIRED in production
    # Application will fail to start if not set
    SECRET_KEY = get_env("SECRET_KEY", required=True)
    
    # Force secure cookies (HTTPS only)
    # Cannot be disabled in production
    SESSION_COOKIE_SECURE = True
    
    # Force CSRF protection
    # Cannot be disabled in production
    WTF_CSRF_ENABLED = True
    
    # ========================================
    # Rate Limiting - Redis Required
    # ========================================
    # Production REQUIRES Redis for rate limiting across multiple workers.
    # If not using Redis, set RATELIMIT_ENABLED=false and implement
    # alternative rate limiting at the reverse proxy level (nginx, etc.)
    #
    # Example Redis URLs:
    #   - Local: redis://localhost:6379/0
    #   - Auth:  redis://user:password@host:6379/0
    #   - SSL:   rediss://host:6379/0
    #
    # WARNING: memory:// storage will NOT work correctly with multiple
    # workers (Gunicorn, uWSGI) as each worker has its own memory space.
    
    RATELIMIT_STORAGE_URL = get_env(
        "RATELIMIT_STORAGE_URL",
        default="redis://localhost:6379/0"
    )
