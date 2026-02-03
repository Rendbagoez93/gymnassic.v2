"""
Environment Utilities Module

Provides utility functions and constants for environment management.
Works alongside Pydantic Settings for specialized environment operations.

Note: Basic configuration now uses Pydantic Settings in config.py.
This module provides additional utilities for edge cases and testing.
"""

import os
from pathlib import Path

# Get the base directory (project root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Define environment types
class Environment:
    """Environment type constants."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


def get_current_environment() -> str:
    """
    Get the current environment from FLASK_ENV or FLASK_APP_ENV.

    Returns:
        str: Current environment (development, production, or testing)
    """
    return os.getenv("FLASK_ENV") or os.getenv("FLASK_APP_ENV", Environment.DEVELOPMENT)


def get_env_file_path(env_name: str | None = None) -> Path:
    """
    Get the path to the environment file for a given environment.

    Args:
        env_name: Environment name. If None, uses current environment.

    Returns:
        Path: Path to the .env file
    """
    if env_name is None:
        env_name = get_current_environment()

    env_files = {
        Environment.DEVELOPMENT: BASE_DIR / ".env.development",
        Environment.PRODUCTION: BASE_DIR / ".env.production",
        Environment.TESTING: BASE_DIR / ".env.testing",
    }

    env_file = env_files.get(env_name, BASE_DIR / ".env")

    # If specific env file doesn't exist, try default .env
    if not env_file.exists():
        default_env = BASE_DIR / ".env"
        if default_env.exists():
            return default_env

    return env_file


def is_development() -> bool:
    """Check if running in development environment."""
    return get_current_environment() == Environment.DEVELOPMENT


def is_production() -> bool:
    """Check if running in production environment."""
    return get_current_environment() == Environment.PRODUCTION


def is_testing() -> bool:
    """Check if running in testing environment."""
    return get_current_environment() == Environment.TESTING


def ensure_directory_exists(path: Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Path to the directory

    Returns:
        Path: The directory path
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
