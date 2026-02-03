"""
Test Flask Application Integration

Tests for Flask application factory and configuration integration.
"""

import pytest
from flask import Flask

from app import create_app
from app.settings import Environment


class TestCreateApp:
    """Test Flask application factory."""

    def test_create_app_returns_flask_instance(self):
        """Test that create_app returns a Flask instance."""
        app = create_app()

        assert isinstance(app, Flask)

    def test_create_app_default_configuration(self):
        """Test that create_app uses DevelopmentConfig by default."""
        app = create_app()

        assert app.config["ENV"] == Environment.DEVELOPMENT
        assert app.config["DEBUG"] is True

    def test_create_app_development_config(self):
        """Test create_app with development configuration."""
        app = create_app(Environment.DEVELOPMENT)

        assert app.config["ENV"] == Environment.DEVELOPMENT
        assert app.config["DEBUG"] is True
        assert app.config["SQLALCHEMY_ECHO"] is True

    def test_create_app_testing_config(self):
        """Test create_app with testing configuration."""
        app = create_app(Environment.TESTING)

        assert app.config["ENV"] == Environment.TESTING
        assert app.config["TESTING"] is True
        assert app.config["WTF_CSRF_ENABLED"] is False

    def test_create_app_config_values(self):
        """Test that app config contains expected values."""
        app = create_app()

        assert "APP_NAME" in app.config
        assert "APP_VERSION" in app.config
        assert "SECRET_KEY" in app.config
        assert "SQLALCHEMY_DATABASE_URI" in app.config

    def test_create_app_sqlalchemy_uri(self):
        """Test that SQLALCHEMY_DATABASE_URI is set correctly."""
        app = create_app()

        assert "SQLALCHEMY_DATABASE_URI" in app.config
        assert app.config["SQLALCHEMY_DATABASE_URI"] is not None

    def test_create_app_sqlalchemy_engine_options(self):
        """Test that SQLALCHEMY_ENGINE_OPTIONS is set correctly."""
        app = create_app()

        assert "SQLALCHEMY_ENGINE_OPTIONS" in app.config
        assert isinstance(app.config["SQLALCHEMY_ENGINE_OPTIONS"], dict)


class TestAppContext:
    """Test Flask application context."""

    def test_app_context(self):
        """Test that app context works correctly."""
        app = create_app()

        with app.app_context():
            assert app.config["APP_NAME"] == "Gymnassic"

    def test_app_config_access(self):
        """Test accessing config from app context."""
        app = create_app()

        with app.app_context():
            assert "DATABASE_URL" in app.config or "SQLALCHEMY_DATABASE_URI" in app.config


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app(Environment.TESTING)
    yield app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


class TestAppFixtures:
    """Test Flask app fixtures."""

    def test_app_fixture(self, app):
        """Test app fixture."""
        assert isinstance(app, Flask)
        assert app.config["TESTING"] is True

    def test_client_fixture(self, client):
        """Test client fixture."""
        assert client is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
