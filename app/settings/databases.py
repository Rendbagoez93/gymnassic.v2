"""
Database Utilities Module

Provides utility functions for database operations and connection management.
Configuration is now handled by Pydantic Settings in config.py.

This module provides helpers for database setup, testing, and migrations.
"""

from pathlib import Path
from typing import Any

from .envcommon import BASE_DIR


def get_sqlite_path(db_name: str = "gymnassic.db") -> str:
    """
    Get the path for a SQLite database file.

    Args:
        db_name: Database filename

    Returns:
        str: SQLite URI string
    """
    db_path = BASE_DIR / "instance" / db_name
    return f"sqlite:///{db_path}"


def get_postgresql_uri(
    username: str,
    password: str,
    host: str = "localhost",
    port: int = 5432,
    database: str = "gymnassic_db",
) -> str:
    """
    Build a PostgreSQL connection URI.

    Args:
        username: Database username
        password: Database password
        host: Database host
        port: Database port
        database: Database name

    Returns:
        str: PostgreSQL URI string
    """
    return f"postgresql://{username}:{password}@{host}:{port}/{database}"


def get_sqlite_engine_options() -> dict[str, Any]:
    """
    Get recommended engine options for SQLite.

    Returns:
        dict: SQLAlchemy engine options for SQLite
    """
    return {
        "pool_pre_ping": True,
        "connect_args": {
            "check_same_thread": False,  # Allow multi-threading
        },
    }


def get_postgresql_engine_options(
    pool_size: int = 10,
    max_overflow: int = 20,
    pool_recycle: int = 3600,
    pool_timeout: int = 30,
    connect_timeout: int = 10,
    app_name: str = "gymnassic",
) -> dict[str, Any]:
    """
    Get recommended engine options for PostgreSQL.

    Args:
        pool_size: Number of connections to keep in pool
        max_overflow: Maximum overflow connections
        pool_recycle: Connection recycle time in seconds
        pool_timeout: Pool checkout timeout in seconds
        connect_timeout: Database connection timeout in seconds
        app_name: Application name for monitoring

    Returns:
        dict: SQLAlchemy engine options for PostgreSQL
    """
    return {
        "pool_size": pool_size,
        "max_overflow": max_overflow,
        "pool_recycle": pool_recycle,
        "pool_pre_ping": True,
        "pool_timeout": pool_timeout,
        "connect_args": {
            "connect_timeout": connect_timeout,
            "application_name": app_name,
        },
    }


def ensure_instance_directory() -> Path:
    """
    Ensure the instance directory exists for SQLite databases.

    Returns:
        Path: Path to instance directory
    """
    instance_dir = BASE_DIR / "instance"
    instance_dir.mkdir(parents=True, exist_ok=True)
    return instance_dir
