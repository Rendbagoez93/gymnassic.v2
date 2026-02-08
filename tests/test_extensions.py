"""
Test Flask Extensions Module

Tests for Flask extensions initialization and configuration.
"""

import pytest
from flask import Flask

from app import create_app
from app.extensions import (
    csrf,
    db,
    init_extensions,
    limiter,
    login_manager,
    mail,
    migrate,
    pwd_context,
    talisman,
)
from app.settings import Environment


class TestExtensionInstances:
    """Test that extension instances are created."""

    def test_db_instance(self):
        """Test SQLAlchemy instance exists."""
        assert db is not None
        assert hasattr(db, "Model")
        assert hasattr(db, "session")

    def test_migrate_instance(self):
        """Test Flask-Migrate instance exists."""
        assert migrate is not None

    def test_login_manager_instance(self):
        """Test Flask-Login instance exists."""
        assert login_manager is not None
        assert hasattr(login_manager, "login_view")

    def test_csrf_instance(self):
        """Test CSRF protection instance exists."""
        assert csrf is not None

    def test_limiter_instance(self):
        """Test rate limiter instance exists."""
        assert limiter is not None

    def test_talisman_instance(self):
        """Test Talisman instance exists."""
        assert talisman is not None

    def test_mail_instance(self):
        """Test Flask-Mail instance exists."""
        assert mail is not None

    def test_pwd_context_instance(self):
        """Test password context instance exists."""
        assert pwd_context is not None
        assert hasattr(pwd_context, "hash")
        assert hasattr(pwd_context, "verify")


class TestInitExtensions:
    """Test init_extensions function."""

    def test_init_extensions_with_development_app(self):
        """Test initializing extensions with development config."""
        app = create_app(Environment.DEVELOPMENT)

        assert app is not None

        # Check that extensions are initialized
        assert "sqlalchemy" in app.extensions
        assert hasattr(app, "login_manager") or "login_manager" in app.extensions # Flask-Login loaded

    def test_init_extensions_with_testing_app(self):
        """Test initializing extensions with testing config."""
        app = create_app(Environment.TESTING)

        assert app is not None
        assert "sqlalchemy" in app.extensions

    def test_database_extension_initialized(self):
        """Test that database extension is properly initialized."""
        app = create_app(Environment.TESTING)

        with app.app_context():
            assert hasattr(db, "engine")
            assert db.engine is not None

    def test_csrf_protection_configured(self):
        """Test that CSRF protection is configured."""
        app = create_app(Environment.DEVELOPMENT)

        # CSRF should be enabled in development
        assert app.config.get("WTF_CSRF_ENABLED") is True

    def test_csrf_disabled_in_testing(self):
        """Test that CSRF is disabled in testing environment."""
        app = create_app(Environment.TESTING)

        # CSRF should be disabled in testing
        assert app.config.get("WTF_CSRF_ENABLED") is False

    def test_rate_limiting_enabled_in_development(self):
        """Test that rate limiting is enabled in development."""
        app = create_app(Environment.DEVELOPMENT)

        assert app.config.get("RATELIMIT_ENABLED") is True

    def test_rate_limiting_disabled_in_testing(self):
        """Test that rate limiting is disabled in testing."""
        app = create_app(Environment.TESTING)

        assert app.config.get("RATELIMIT_ENABLED") is False

    def test_mail_extension_configured(self):
        """Test that mail extension is configured."""
        app = create_app(Environment.DEVELOPMENT)

        assert app.config.get("MAIL_SERVER") is not None
        assert app.config.get("MAIL_PORT") is not None
        assert app.config.get("MAIL_DEFAULT_SENDER") is not None

    def test_login_manager_configured(self):
        """Test that login manager is configured."""
        app = create_app(Environment.DEVELOPMENT)

        assert login_manager.login_view is not None or app.config.get("LOGIN_VIEW") is not None


class TestPasswordContext:
    """Test password hashing context."""

    def test_password_hashing(self):
        """Test password hashing works."""
        password = "TestPassword123!"

        hashed = pwd_context.hash(password)

        assert hashed != password
        assert hashed.startswith("$2b$")  # bcrypt hash
        assert len(hashed) == 60  # bcrypt produces 60-char hash

    def test_password_verification(self):
        """Test password verification works."""
        password = "TestPassword123!"

        hashed = pwd_context.hash(password)

        assert pwd_context.verify(password, hashed) is True
        assert pwd_context.verify("wrong_password", hashed) is False

    def test_password_hashing_unique(self):
        """Test that hashing same password produces different hashes."""
        password = "TestPassword123!"

        hash1 = pwd_context.hash(password)
        hash2 = pwd_context.hash(password)

        # Hashes should be different due to salt
        assert hash1 != hash2
        # But both should verify correctly
        assert pwd_context.verify(password, hash1) is True
        assert pwd_context.verify(password, hash2) is True

    def test_bcrypt_scheme_configured(self):
        """Test that bcrypt is configured as password scheme."""
        assert "bcrypt" in pwd_context.schemes()


class TestExtensionsAllExport:
    """Test __all__ export list."""

    def test_all_exports_exist(self):
        """Test that all exported names are defined."""
        from app import extensions

        for name in extensions.__all__:
            assert hasattr(extensions, name), f"{name} not found in extensions module"

    def test_essential_extensions_exported(self):
        """Test that essential extensions are exported."""
        from app import extensions

        essential = [
            "db",
            "migrate",
            "login_manager",
            "csrf",
            "limiter",
            "mail",
            "pwd_context",
            "init_extensions",
        ]

        for ext in essential:
            assert ext in extensions.__all__, f"{ext} not in __all__"


class TestExtensionsIntegration:
    """Test extensions integration with Flask app."""

    @pytest.fixture
    def app(self):
        """Create a test Flask application."""
        app = create_app(Environment.TESTING)
        return app

    @pytest.fixture
    def client(self, app):
        """Create a test client."""
        return app.test_client()

    def test_database_context(self, app):
        """Test database context works."""
        with app.app_context():
            # Should not raise any errors
            assert db.engine is not None

    def test_extensions_registered_in_app(self, app):
        """Test that extensions are registered in app.extensions."""
        assert "sqlalchemy" in app.extensions
        # migrate adds itself to extensions as well
        assert len(app.extensions) > 0

    def test_app_config_accessible(self, app):
        """Test that app config is accessible and contains extension config."""
        assert "SQLALCHEMY_DATABASE_URI" in app.config
        assert "WTF_CSRF_ENABLED" in app.config
        assert "MAIL_SERVER" in app.config


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
