"""
Dependency Injection Containers

This module defines dependency injection containers using dependency-injector.
Containers provide centralized configuration and dependency management for the application.
"""

from dependency_injector import containers, providers

from app.settings.config import get_config


class ApplicationContainer(containers.DeclarativeContainer):
    """Main application container for dependency injection."""

    # Configuration
    config = providers.Singleton(get_config)

    # Add other providers as the application grows
    # database = providers.Singleton(Database, config=config.provided.DATABASE_URL)
    # cache = providers.Singleton(Cache, config=config.provided.CACHE_URL)
    # email_service = providers.Factory(EmailService, config=config)
