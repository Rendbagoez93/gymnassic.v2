"""
Settings Package

Centralized configuration management for Gymnassic application.
"""

from .config import (
    BaseConfig,
    DevelopmentConfig,
    Environment,
    ProductionConfig,
    TestingConfig,
    config,
    get_config,
)
from .containers import ApplicationContainer
from .databases import DatabaseConfig, DatabaseEngine
from .envcommon import BASE_DIR, get_current_environment, is_development, is_production
from .gymconf import GymConfig

__all__ = [
    # Configuration classes
    "BaseConfig",
    "DevelopmentConfig",
    "ProductionConfig",
    "TestingConfig",
    "Environment",
    "get_config",
    "config",
    # Dependency injection
    "ApplicationContainer",
    # Database configuration
    "DatabaseConfig",
    "DatabaseEngine",
    # Environment utilities
    "BASE_DIR",
    "get_current_environment",
    "is_development",
    "is_production",
    # Gym configuration
    "GymConfig",
]
