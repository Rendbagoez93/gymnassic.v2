"""
Test Security Utilities Module

Tests for security utility functions.
"""

import pytest

from app.settings.security import (
    generate_secret_key,
    get_rate_limit_key,
    sanitize_redirect_url,
    validate_password_strength,
)


class TestGenerateSecretKey:
    """Test generate_secret_key function."""

    def test_generate_secret_key_default(self):
        """Test generating secret key with default length."""
        key = generate_secret_key()
        assert isinstance(key, str)
        assert len(key) == 64  # 32 bytes = 64 hex characters

    def test_generate_secret_key_custom_length(self):
        """Test generating secret key with custom length."""
        key = generate_secret_key(16)
        assert isinstance(key, str)
        assert len(key) == 32  # 16 bytes = 32 hex characters

    def test_generate_secret_key_unique(self):
        """Test that generated keys are unique."""
        key1 = generate_secret_key()
        key2 = generate_secret_key()
        assert key1 != key2


class TestValidatePasswordStrength:
    """Test validate_password_strength function."""

    def test_validate_password_strong(self):
        """Test validating a strong password."""
        is_valid, errors = validate_password_strength("StrongP@ss123")
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_password_too_short(self):
        """Test password that's too short."""
        is_valid, errors = validate_password_strength("Sh0rt!")
        assert is_valid is False
        assert any("at least 8 characters" in err for err in errors)

    def test_validate_password_no_uppercase(self):
        """Test password without uppercase."""
        is_valid, errors = validate_password_strength("password123!")
        assert is_valid is False
        assert any("uppercase" in err for err in errors)

    def test_validate_password_no_lowercase(self):
        """Test password without lowercase."""
        is_valid, errors = validate_password_strength("PASSWORD123!")
        assert is_valid is False
        assert any("lowercase" in err for err in errors)

    def test_validate_password_no_numbers(self):
        """Test password without numbers."""
        is_valid, errors = validate_password_strength("Password!@#")
        assert is_valid is False
        assert any("number" in err for err in errors)

    def test_validate_password_no_special(self):
        """Test password without special characters."""
        is_valid, errors = validate_password_strength("Password123")
        assert is_valid is False
        assert any("special character" in err for err in errors)

    def test_validate_password_custom_requirements(self):
        """Test password validation with custom requirements."""
        is_valid, errors = validate_password_strength(
            "simple",
            min_length=4,
            require_uppercase=False,
            require_lowercase=True,
            require_numbers=False,
            require_special=False,
        )
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_password_multiple_errors(self):
        """Test password with multiple validation errors."""
        is_valid, errors = validate_password_strength("abc")
        assert is_valid is False
        assert len(errors) > 1


class TestGetRateLimitKey:
    """Test get_rate_limit_key function."""

    def test_get_rate_limit_key_with_user_id_int(self):
        """Test rate limit key with integer user ID."""
        key = get_rate_limit_key(123, "login")
        assert key == "ratelimit:user:123:login"

    def test_get_rate_limit_key_with_user_id_str(self):
        """Test rate limit key with string user ID."""
        key = get_rate_limit_key("user123", "api_call")
        assert key == "ratelimit:user:user123:api_call"

    def test_get_rate_limit_key_anonymous(self):
        """Test rate limit key for anonymous user."""
        key = get_rate_limit_key(None, "signup")
        assert key == "ratelimit:anonymous:signup"


class TestSanitizeRedirectUrl:
    """Test sanitize_redirect_url function."""

    def test_sanitize_redirect_url_relative(self):
        """Test sanitizing relative URL."""
        url = sanitize_redirect_url("/dashboard")
        assert url == "/dashboard"

    def test_sanitize_redirect_url_relative_with_query(self):
        """Test sanitizing relative URL with query parameters."""
        url = sanitize_redirect_url("/dashboard?foo=bar")
        assert url == "/dashboard?foo=bar"

    def test_sanitize_redirect_url_empty(self):
        """Test sanitizing empty URL."""
        url = sanitize_redirect_url("")
        assert url is None

    def test_sanitize_redirect_url_absolute_not_allowed(self):
        """Test that absolute URLs are rejected by default."""
        url = sanitize_redirect_url("https://example.com/path")
        assert url is None

    def test_sanitize_redirect_url_absolute_allowed_host(self):
        """Test absolute URL with allowed host."""
        url = sanitize_redirect_url(
            "https://example.com/path", allowed_hosts=["example.com"]
        )
        assert url == "https://example.com/path"

    def test_sanitize_redirect_url_absolute_disallowed_host(self):
        """Test absolute URL with disallowed host."""
        url = sanitize_redirect_url(
            "https://evil.com/path", allowed_hosts=["example.com"]
        )
        assert url is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
