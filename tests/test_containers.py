"""
Test Dependency Injection Containers

Tests for the dependency injection container configuration.
"""

import pytest

from app.settings import ApplicationContainer, DevelopmentConfig


class TestApplicationContainer:
    """Test ApplicationContainer dependency injection."""

    def test_container_creation(self):
        """Test that container can be created."""
        container = ApplicationContainer()

        assert container is not None

    def test_container_config_provider(self):
        """Test that container provides config."""
        container = ApplicationContainer()

        config = container.config()

        assert config is not None
        assert hasattr(config, "APP_NAME")
        assert hasattr(config, "DEBUG")

    def test_container_config_singleton(self):
        """Test that config is a singleton."""
        container = ApplicationContainer()

        config1 = container.config()
        config2 = container.config()

        assert config1 is config2

    def test_container_provides_development_config_by_default(self):
        """Test that container provides DevelopmentConfig by default."""
        container = ApplicationContainer()

        config = container.config()

        assert isinstance(config, DevelopmentConfig)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
