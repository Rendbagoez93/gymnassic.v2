"""
Test Configuration Module

Tests for configuration settings using pydantic-settings.
"""

import json
import os
from pathlib import Path

import pytest

from app.settings import (
    BaseConfig,
    DevelopmentConfig,
    Environment,
    ProductionConfig,
    TestingConfig,
    get_config,
)


class TestBaseConfig:
    """Test BaseConfig default values and validation."""

    def test_base_config_defaults(self):
        """Test that BaseConfig has correct default values."""
        # Clear environment variables that might override defaults
        env_backup = {}
        keys_to_clear = ["DEBUG", "TESTING", "ENV"]
        for key in keys_to_clear:
            env_backup[key] = os.environ.pop(key, None)

        try:
            config = BaseConfig(_env_file=None)  # Don't load from .env file

            assert config.APP_NAME == "Gymnassic"
            assert config.APP_VERSION == "2.0.0"
            assert config.DEBUG is False
            assert config.TESTING is False
            assert config.ENV == Environment.DEVELOPMENT
        finally:
            # Restore environment
            for key, value in env_backup.items():
                if value is not None:
                    os.environ[key] = value

    def test_base_config_paths(self):
        """Test that path configurations are correct."""
        config = BaseConfig()

        assert isinstance(config.BASE_DIR, Path)
        assert isinstance(config.INSTANCE_PATH, Path)
        assert config.TEMPLATE_FOLDER == "templates"
        assert config.STATIC_FOLDER == "static"
        assert config.STATIC_URL_PATH == "/static"

    def test_base_config_database_defaults(self):
        """Test database configuration defaults."""
        config = BaseConfig()

        assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
        assert config.SQLALCHEMY_ECHO is False
        assert config.DB_POOL_PRE_PING is True

    def test_base_config_security_defaults(self):
        """Test security configuration defaults."""
        config = BaseConfig()

        assert config.SESSION_COOKIE_HTTPONLY is True
        assert config.SESSION_COOKIE_SAMESITE == "Lax"
        assert config.WTF_CSRF_ENABLED is True
        assert config.PASSWORD_MIN_LENGTH == 8
        assert config.PASSWORD_REQUIRE_UPPERCASE is True

    def test_base_config_sqlalchemy_uri_property(self):
        """Test SQLALCHEMY_DATABASE_URI property."""
        config = BaseConfig()

        assert config.SQLALCHEMY_DATABASE_URI == config.DATABASE_URL
        assert "sqlite" in config.SQLALCHEMY_DATABASE_URI.lower()

    def test_base_config_engine_options_sqlite(self):
        """Test SQLAlchemy engine options for SQLite."""
        config = BaseConfig()

        engine_options = config.SQLALCHEMY_ENGINE_OPTIONS
        assert "pool_pre_ping" in engine_options
        assert "connect_args" in engine_options
        assert engine_options["connect_args"]["check_same_thread"] is False

    def test_base_config_engine_options_postgresql(self):
        """Test SQLAlchemy engine options for PostgreSQL."""
        config = BaseConfig(DATABASE_URL="postgresql://localhost/test")

        engine_options = config.SQLALCHEMY_ENGINE_OPTIONS
        assert "pool_size" in engine_options
        assert "max_overflow" in engine_options
        assert "pool_recycle" in engine_options
        assert engine_options["pool_size"] == 10
        assert engine_options["max_overflow"] == 20

    def test_base_config_email_defaults(self):
        """Test email configuration defaults."""
        config = BaseConfig()

        assert config.MAIL_SERVER == "localhost"
        assert config.MAIL_PORT == 587
        assert config.MAIL_USE_TLS is True
        assert config.MAIL_DEFAULT_SENDER == "noreply@gymnassic.com"

    def test_base_config_feature_flags(self):
        """Test feature flag defaults."""
        config = BaseConfig()

        assert config.FEATURE_ONLINE_PAYMENT is False
        assert config.FEATURE_EMAIL_NOTIFICATIONS is True
        assert config.FEATURE_SMS_NOTIFICATIONS is False


class TestDevelopmentConfig:
    """Test DevelopmentConfig overrides."""

    def test_development_environment(self):
        """Test development environment settings."""
        config = DevelopmentConfig()

        assert config.ENV == Environment.DEVELOPMENT
        assert config.DEBUG is True
        assert config.SQLALCHEMY_ECHO is True

    def test_development_security_relaxed(self):
        """Test that security is relaxed in development."""
        config = DevelopmentConfig()

        assert config.SESSION_COOKIE_SECURE is False

    def test_development_logging(self):
        """Test development logging settings."""
        config = DevelopmentConfig()

        assert config.LOG_LEVEL == "DEBUG"

    def test_development_email_suppressed(self):
        """Test that email sending is suppressed in development."""
        config = DevelopmentConfig()

        assert config.MAIL_SUPPRESS_SEND is True

    def test_development_no_caching(self):
        """Test that static file caching is disabled in development."""
        config = DevelopmentConfig()

        assert config.SEND_FILE_MAX_AGE_DEFAULT == 0


class TestProductionConfig:
    """Test ProductionConfig overrides."""

    def test_production_environment(self):
        """Test production environment settings."""
        # Set SECRET_KEY env var to avoid validation error
        os.environ["SECRET_KEY"] = "test-production-secret-key-12345678"
        config = ProductionConfig()

        assert config.ENV == Environment.PRODUCTION
        assert config.DEBUG is False
        assert config.SQLALCHEMY_ECHO is False

        # Clean up
        del os.environ["SECRET_KEY"]

    def test_production_security_enforced(self):
        """Test that security is enforced in production."""
        os.environ["SECRET_KEY"] = "test-production-secret-key-12345678"
        config = ProductionConfig()

        assert config.SESSION_COOKIE_SECURE is True
        assert config.WTF_CSRF_ENABLED is True
        assert config.REMEMBER_COOKIE_SECURE is True
        assert config.PREFERRED_URL_SCHEME == "https"

        del os.environ["SECRET_KEY"]

    def test_production_secret_key_validation(self):
        """Test that production requires a valid SECRET_KEY."""
        # Clear SECRET_KEY from environment to test validation
        secret_backup = os.environ.pop("SECRET_KEY", None)

        try:
            # Should raise validation error when SECRET_KEY is not provided
            # and we're using default value in production
            from pydantic import ValidationError

            with pytest.raises(ValidationError):
                config = ProductionConfig(_env_file=None)
                # Access SECRET_KEY to trigger validation
                _ = config.SECRET_KEY
        finally:
            # Restore environment
            if secret_backup is not None:
                os.environ["SECRET_KEY"] = secret_backup

    def test_production_logging(self):
        """Test production logging settings."""
        os.environ["SECRET_KEY"] = "test-production-secret-key-12345678"
        config = ProductionConfig()

        assert config.LOG_LEVEL == "WARNING"

        del os.environ["SECRET_KEY"]

    def test_production_email_enabled(self):
        """Test that email sending is enabled in production."""
        os.environ["SECRET_KEY"] = "test-production-secret-key-12345678"
        config = ProductionConfig()

        assert config.MAIL_SUPPRESS_SEND is False

        del os.environ["SECRET_KEY"]

    def test_production_long_caching(self):
        """Test that static file caching is enabled in production."""
        os.environ["SECRET_KEY"] = "test-production-secret-key-12345678"
        config = ProductionConfig()

        assert config.SEND_FILE_MAX_AGE_DEFAULT == 31536000  # 1 year

        del os.environ["SECRET_KEY"]

    def test_production_features(self):
        """Test production feature flags."""
        os.environ["SECRET_KEY"] = "test-production-secret-key-12345678"
        config = ProductionConfig()

        assert config.FEATURE_ONLINE_PAYMENT is True

        del os.environ["SECRET_KEY"]


class TestTestingConfig:
    """Test TestingConfig overrides."""

    def test_testing_environment(self):
        """Test testing environment settings."""
        config = TestingConfig()

        assert config.ENV == Environment.TESTING
        assert config.TESTING is True
        assert config.DEBUG is True

    def test_testing_database_in_memory(self):
        """Test that testing uses in-memory database."""
        config = TestingConfig()

        assert config.DATABASE_URL == "sqlite:///:memory:"
        assert ":memory:" in config.SQLALCHEMY_DATABASE_URI

    def test_testing_csrf_disabled(self):
        """Test that CSRF is disabled in testing."""
        config = TestingConfig()

        assert config.WTF_CSRF_ENABLED is False

    def test_testing_rate_limiting_disabled(self):
        """Test that rate limiting is disabled in testing."""
        config = TestingConfig()

        assert config.RATELIMIT_ENABLED is False

    def test_testing_fast_passwords(self):
        """Test that password requirements are relaxed for testing."""
        config = TestingConfig()

        assert config.PASSWORD_MIN_LENGTH == 4


class TestGetConfig:
    """Test get_config function."""

    def test_get_config_default(self):
        """Test get_config returns DevelopmentConfig by default."""
        config = get_config()

        assert isinstance(config, DevelopmentConfig)

    def test_get_config_development(self):
        """Test get_config with development environment."""
        config = get_config(Environment.DEVELOPMENT)

        assert isinstance(config, DevelopmentConfig)

    def test_get_config_production(self):
        """Test get_config with production environment."""
        os.environ["SECRET_KEY"] = "test-production-secret-key-12345678"
        config = get_config(Environment.PRODUCTION)

        assert isinstance(config, ProductionConfig)

        del os.environ["SECRET_KEY"]

    def test_get_config_testing(self):
        """Test get_config with testing environment."""
        config = get_config(Environment.TESTING)

        assert isinstance(config, TestingConfig)

    def test_get_config_from_env_variable(self):
        """Test get_config reads from FLASK_ENV environment variable."""
        os.environ["FLASK_ENV"] = Environment.TESTING
        config = get_config()

        assert isinstance(config, TestingConfig)

        del os.environ["FLASK_ENV"]


class TestConfigEnvironmentVariables:
    """Test configuration with environment variables."""

    def test_config_from_env_variables(self):
        """Test that configuration reads from environment variables."""
        os.environ["APP_NAME"] = "TestGym"
        os.environ["DEBUG"] = "true"
        os.environ["TIMEZONE"] = "America/New_York"

        config = BaseConfig()

        assert config.APP_NAME == "TestGym"
        assert config.DEBUG is True
        assert config.TIMEZONE == "America/New_York"

        # Clean up
        del os.environ["APP_NAME"]
        del os.environ["DEBUG"]
        del os.environ["TIMEZONE"]

    def test_config_integer_from_env(self):
        """Test integer configuration from environment variables."""
        os.environ["MAIL_PORT"] = "2525"
        os.environ["PASSWORD_MIN_LENGTH"] = "12"

        config = BaseConfig()

        assert config.MAIL_PORT == 2525
        assert config.PASSWORD_MIN_LENGTH == 12

        del os.environ["MAIL_PORT"]
        del os.environ["PASSWORD_MIN_LENGTH"]

    def test_config_boolean_from_env(self):
        """Test boolean configuration from environment variables."""
        os.environ["MAIL_USE_TLS"] = "false"
        os.environ["FEATURE_SMS_NOTIFICATIONS"] = "true"

        config = BaseConfig()

        assert config.MAIL_USE_TLS is False
        assert config.FEATURE_SMS_NOTIFICATIONS is True

        del os.environ["MAIL_USE_TLS"]
        del os.environ["FEATURE_SMS_NOTIFICATIONS"]


class TestGymConfigIntegration:
    """Test gym configuration integration with main config."""

    def test_gym_config_path_default(self):
        """Test default gym config path."""
        config = BaseConfig()
        assert "gym_profile.json" in config.GYM_CONFIG_PATH

    def test_gym_config_loading_when_file_exists(self, tmp_path):
        """Test loading gym config when file exists."""
        # Create temporary gym profile
        gym_data = {
            "gym_name": "Test Integration Gym",
            "contact": {"email": "test@integration.com"},
            "facilities": ["Weights", "Cardio"],
        }

        gym_file = tmp_path / "gym_profile.json"
        with open(gym_file, "w") as f:
            json.dump(gym_data, f)

        # Update config to use temp file
        os.environ["GYM_CONFIG_PATH"] = str(gym_file)

        try:
            config = BaseConfig()
            gym_config = config.gym_config

            assert gym_config is not None
            assert gym_config.gym_name == "Test Integration Gym"
            assert gym_config.contact.email == "test@integration.com"
            assert "Weights" in gym_config.facilities
        finally:
            del os.environ["GYM_CONFIG_PATH"]

    def test_gym_config_returns_none_when_file_missing(self):
        """Test gym_config returns None when file doesn't exist."""
        os.environ["GYM_CONFIG_PATH"] = "/non/existent/path.json"

        try:
            config = BaseConfig()
            gym_config = config.gym_config

            assert gym_config is None
        finally:
            del os.environ["GYM_CONFIG_PATH"]

    def test_gym_config_accessible_from_all_environments(self, tmp_path):
        """Test gym config works in all environment configs."""
        # Create gym profile
        gym_data = {
            "gym_name": "Multi-Env Gym",
            "contact": {"email": "multi@env.com"},
        }

        gym_file = tmp_path / "multi_env.json"
        with open(gym_file, "w") as f:
            json.dump(gym_data, f)

        os.environ["GYM_CONFIG_PATH"] = str(gym_file)

        try:
            # Test in development
            dev_config = DevelopmentConfig()
            assert dev_config.gym_config.gym_name == "Multi-Env Gym"

            # Test in testing
            test_config = TestingConfig()
            assert test_config.gym_config.gym_name == "Multi-Env Gym"

            # Test in production (need to set SECRET_KEY for production)
            os.environ["SECRET_KEY"] = "test-secret-key-for-production"
            prod_config = ProductionConfig()
            assert prod_config.gym_config.gym_name == "Multi-Env Gym"
        finally:
            del os.environ["GYM_CONFIG_PATH"]
            if "SECRET_KEY" in os.environ:
                del os.environ["SECRET_KEY"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
