"""
Environment Configuration Module

This module manages environment variables and settings using python-dotenv.
It defines different environments (Development, Production) and loads
appropriate configuration based on FLASK_ENV environment variable.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# Get the base directory (project root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Define environment types
class Environment:
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


def get_env_file() -> Path:
    flask_env = os.getenv("FLASK_ENV", Environment.DEVELOPMENT)
    
    env_files = {
        Environment.DEVELOPMENT: BASE_DIR / ".env.development",
        Environment.PRODUCTION: BASE_DIR / ".env.production",
        Environment.TESTING: BASE_DIR / ".env.testing",
    }
    
    # Return specific env file or fallback to default .env
    env_file = env_files.get(flask_env, BASE_DIR / ".env")
    
    # If specific env file doesn't exist, try default .env
    if not env_file.exists():
        default_env = BASE_DIR / ".env"
        if default_env.exists():
            return default_env
    
    return env_file


def load_environment():
    env_file = get_env_file()
    
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✓ Loaded environment from: {env_file}")
    else:
        print(f"⚠ Warning: No environment file found at {env_file}")
        print(f"  Using system environment variables only")


def get_env(key: str, default: str = None, required: bool = False) -> str:
    value = os.getenv(key, default)
    
    if required and value is None:
        raise EnvironmentError(
            f"Required environment variable '{key}' is not set. "
            f"Please add it to your .env file."
        )
    
    return value


def get_bool_env(key: str, default: bool = False) -> bool:
    value = os.getenv(key, str(default)).lower()
    return value in ("true", "1", "yes", "on")


def get_int_env(key: str, default: int = 0) -> int:
    value = os.getenv(key, str(default))
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


# Load environment on module import
load_environment()
