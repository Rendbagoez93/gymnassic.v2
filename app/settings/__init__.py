"""
Settings Package

Centralized configuration management for Gymnassic application.
"""

from .config import (
    BaseConfig,
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
    get_config,
    config,
)
from .envcommon import Environment, load_environment, get_env, get_bool_env, get_int_env
from .security import SecurityConfig, DevelopmentSecurityConfig, ProductionSecurityConfig
from .databases import DatabaseConfig, SQLiteDatabaseConfig, PostgresDatabaseConfig

__all__ = [
    # Configuration classes
    "BaseConfig",
    "DevelopmentConfig",
    "ProductionConfig",
    "TestingConfig",
    "get_config",
    "config",
    # Environment utilities
    "Environment",
    "load_environment",
    "get_env",
    "get_bool_env",
    "get_int_env",
    # Specific configs
    "SecurityConfig",
    "DevelopmentSecurityConfig",
    "ProductionSecurityConfig",
    "DatabaseConfig",
    "SQLiteDatabaseConfig",
    "PostgresDatabaseConfig",
]
