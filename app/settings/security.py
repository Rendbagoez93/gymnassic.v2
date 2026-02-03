"""
Security Utilities Module

Provides security-related utility functions and helpers.
Configuration is now handled by Pydantic Settings in config.py.

This module provides helpers for password validation, token generation,
and security checks.
"""

import re
import secrets
from typing import Any


def generate_secret_key(length: int = 32) -> str:
    """
    Generate a cryptographically secure secret key.

    Args:
        length: Length of the secret key in bytes

    Returns:
        str: Hexadecimal secret key
    """
    return secrets.token_hex(length)


def validate_password_strength(
    password: str,
    min_length: int = 8,
    require_uppercase: bool = True,
    require_lowercase: bool = True,
    require_numbers: bool = True,
    require_special: bool = True,
) -> tuple[bool, list[str]]:
    """
    Validate password strength based on requirements.

    Args:
        password: Password to validate
        min_length: Minimum password length
        require_uppercase: Require at least one uppercase letter
        require_lowercase: Require at least one lowercase letter
        require_numbers: Require at least one number
        require_special: Require at least one special character

    Returns:
        tuple: (is_valid, list of error messages)
    """
    errors = []

    if len(password) < min_length:
        errors.append(f"Password must be at least {min_length} characters long")

    if require_uppercase and not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter")

    if require_lowercase and not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter")

    if require_numbers and not re.search(r"\d", password):
        errors.append("Password must contain at least one number")

    if require_special and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character")

    return len(errors) == 0, errors


def get_rate_limit_key(user_id: str | int | None, action: str) -> str:
    """
    Generate a rate limit key for a user action.

    Args:
        user_id: User identifier (or None for anonymous)
        action: Action being rate limited

    Returns:
        str: Rate limit key
    """
    if user_id is None:
        return f"ratelimit:anonymous:{action}"
    return f"ratelimit:user:{user_id}:{action}"


def sanitize_redirect_url(url: str, allowed_hosts: list[str] | None = None) -> str | None:
    """
    Sanitize and validate a redirect URL to prevent open redirect vulnerabilities.

    Args:
        url: URL to sanitize
        allowed_hosts: List of allowed hostnames (None = same host only)

    Returns:
        str | None: Sanitized URL or None if invalid
    """
    if not url:
        return None

    # Only allow relative URLs or URLs from allowed hosts
    if url.startswith("/"):
        # Relative URL - safe
        return url

    # For absolute URLs, would need to parse and validate host
    # For now, reject absolute URLs unless explicitly allowed
    if allowed_hosts:
        from urllib.parse import urlparse

        parsed = urlparse(url)
        if parsed.hostname in allowed_hosts:
            return url

    return None


def get_session_config(secure: bool = True) -> dict[str, Any]:
    """
    Get recommended session configuration.

    Args:
        secure: Whether to require HTTPS

    Returns:
        dict: Session configuration
    """
    return {
        "SESSION_COOKIE_SECURE": secure,
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": "Strict" if secure else "Lax",
        "PERMANENT_SESSION_LIFETIME": 3600,  # 1 hour
    }


def get_csrf_config(enabled: bool = True) -> dict[str, Any]:
    """
    Get recommended CSRF configuration.

    Args:
        enabled: Whether CSRF protection is enabled

    Returns:
        dict: CSRF configuration
    """
    return {
        "WTF_CSRF_ENABLED": enabled,
        "WTF_CSRF_TIME_LIMIT": 3600,  # 1 hour
    }
