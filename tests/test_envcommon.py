"""
Test Environment Utilities Module

Tests for environment utilities and helper functions.
"""

import os
from pathlib import Path

import pytest

from app.settings.envcommon import (
    BASE_DIR,
    Environment,
    ensure_directory_exists,
    get_current_environment,
    get_env_file_path,
    is_development,
    is_production,
    is_testing,
)


class TestEnvironmentConstants:
    """Test environment constants."""

    def test_environment_constants(self):
        """Test that environment constants are defined."""
        assert Environment.DEVELOPMENT == "development"
        assert Environment.PRODUCTION == "production"
        assert Environment.TESTING == "testing"

    def test_base_dir_exists(self):
        """Test that BASE_DIR is a valid path."""
        assert isinstance(BASE_DIR, Path)
        assert BASE_DIR.exists()
        assert BASE_DIR.is_dir()


class TestGetCurrentEnvironment:
    """Test get_current_environment function."""

    def test_get_current_environment_default(self):
        """Test default environment."""
        # Save current env vars
        flask_env = os.environ.pop("FLASK_ENV", None)
        flask_app_env = os.environ.pop("FLASK_APP_ENV", None)

        try:
            env = get_current_environment()
            assert env == Environment.DEVELOPMENT
        finally:
            # Restore env vars
            if flask_env:
                os.environ["FLASK_ENV"] = flask_env
            if flask_app_env:
                os.environ["FLASK_APP_ENV"] = flask_app_env

    def test_get_current_environment_from_flask_env(self):
        """Test reading from FLASK_ENV."""
        os.environ["FLASK_ENV"] = Environment.PRODUCTION
        try:
            env = get_current_environment()
            assert env == Environment.PRODUCTION
        finally:
            os.environ.pop("FLASK_ENV", None)

    def test_get_current_environment_from_flask_app_env(self):
        """Test reading from FLASK_APP_ENV."""
        os.environ.pop("FLASK_ENV", None)
        os.environ["FLASK_APP_ENV"] = Environment.TESTING
        try:
            env = get_current_environment()
            assert env == Environment.TESTING
        finally:
            os.environ.pop("FLASK_APP_ENV", None)


class TestGetEnvFilePath:
    """Test get_env_file_path function."""

    def test_get_env_file_path_development(self):
        """Test getting development env file path."""
        path = get_env_file_path(Environment.DEVELOPMENT)
        assert isinstance(path, Path)
        assert path.name == ".env.development" or path.name == ".env"

    def test_get_env_file_path_production(self):
        """Test getting production env file path."""
        path = get_env_file_path(Environment.PRODUCTION)
        assert isinstance(path, Path)
        assert path.name == ".env.production" or path.name == ".env"

    def test_get_env_file_path_testing(self):
        """Test getting testing env file path."""
        path = get_env_file_path(Environment.TESTING)
        assert isinstance(path, Path)
        assert path.name == ".env.testing" or path.name == ".env"

    def test_get_env_file_path_current(self):
        """Test getting current env file path."""
        path = get_env_file_path()
        assert isinstance(path, Path)


class TestEnvironmentCheckers:
    """Test environment checker functions."""

    def test_is_development(self):
        """Test is_development function."""
        os.environ["FLASK_ENV"] = Environment.DEVELOPMENT
        try:
            assert is_development() is True
            assert is_production() is False
            assert is_testing() is False
        finally:
            os.environ.pop("FLASK_ENV", None)

    def test_is_production(self):
        """Test is_production function."""
        os.environ["FLASK_ENV"] = Environment.PRODUCTION
        try:
            assert is_development() is False
            assert is_production() is True
            assert is_testing() is False
        finally:
            os.environ.pop("FLASK_ENV", None)

    def test_is_testing(self):
        """Test is_testing function."""
        os.environ["FLASK_ENV"] = Environment.TESTING
        try:
            assert is_development() is False
            assert is_production() is False
            assert is_testing() is True
        finally:
            os.environ.pop("FLASK_ENV", None)


class TestEnsureDirectoryExists:
    """Test ensure_directory_exists function."""

    def test_ensure_directory_exists_creates_new(self, tmp_path):
        """Test creating a new directory."""
        test_dir = tmp_path / "test_dir"
        assert not test_dir.exists()

        result = ensure_directory_exists(test_dir)

        assert test_dir.exists()
        assert test_dir.is_dir()
        assert result == test_dir

    def test_ensure_directory_exists_existing(self, tmp_path):
        """Test with existing directory."""
        test_dir = tmp_path / "existing_dir"
        test_dir.mkdir()

        result = ensure_directory_exists(test_dir)

        assert test_dir.exists()
        assert result == test_dir

    def test_ensure_directory_exists_nested(self, tmp_path):
        """Test creating nested directories."""
        nested_dir = tmp_path / "level1" / "level2" / "level3"
        assert not nested_dir.exists()

        result = ensure_directory_exists(nested_dir)

        assert nested_dir.exists()
        assert nested_dir.is_dir()
        assert result == nested_dir


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
