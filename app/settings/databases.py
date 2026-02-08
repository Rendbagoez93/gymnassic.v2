"""
Database Engine Configuration

Defines database engine types and their recommended SQLAlchemy configurations.
This keeps the main config.py file focused while centralizing database-specific settings.
"""

from enum import Enum
from typing import Any


class DatabaseEngine(str, Enum):
    """Supported database engine types."""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"


class DatabaseConfig:
    """Database engine configuration and utilities."""

    @staticmethod
    def get_engine_options(
        database_url: str,
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_recycle: int = 3600,
        pool_timeout: int = 30,
        connect_timeout: int = 10,
        app_name: str = "gymnassic",
    ) -> dict[str, Any]:
        """
        Get recommended SQLAlchemy engine options based on database type.

        Args:
            database_url: Database connection URL
            pool_size: Number of connections to keep in pool
            max_overflow: Maximum overflow connections
            pool_recycle: Connection recycle time in seconds
            pool_timeout: Pool checkout timeout in seconds
            connect_timeout: Database connection timeout in seconds
            app_name: Application name for monitoring

        Returns:
            dict: SQLAlchemy engine options appropriate for the database type
        """
        engine_type = DatabaseConfig.detect_engine(database_url)

        if engine_type == DatabaseEngine.SQLITE:
            return DatabaseConfig.get_sqlite_options()
        elif engine_type == DatabaseEngine.POSTGRESQL:
            return DatabaseConfig.get_postgresql_options(
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_recycle=pool_recycle,
                pool_timeout=pool_timeout,
                connect_timeout=connect_timeout,
                app_name=app_name,
            )
        elif engine_type == DatabaseEngine.MYSQL:
            return DatabaseConfig.get_mysql_options(
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_recycle=pool_recycle,
                pool_timeout=pool_timeout,
                connect_timeout=connect_timeout,
            )
        else:
            # Default options for unknown engines
            return {"pool_pre_ping": True}

    @staticmethod
    def detect_engine(database_url: str) -> DatabaseEngine:
        """
        Detect database engine type from connection URL.

        Args:
            database_url: Database connection URL

        Returns:
            DatabaseEngine: Detected engine type
        """
        url_lower = database_url.lower()
        if url_lower.startswith("sqlite"):
            return DatabaseEngine.SQLITE
        elif url_lower.startswith(("postgresql", "postgres")):
            return DatabaseEngine.POSTGRESQL
        elif url_lower.startswith("mysql"):
            return DatabaseEngine.MYSQL
        else:
            # Default to PostgreSQL for unknown schemes
            return DatabaseEngine.POSTGRESQL

    @staticmethod
    def get_sqlite_options() -> dict[str, Any]:
        """
        Get recommended SQLAlchemy engine options for SQLite.

        Returns:
            dict: SQLite-specific engine options
        """
        return {
            "pool_pre_ping": True,
            "connect_args": {
                "check_same_thread": False,  # Allow multi-threading
            },
        }

    @staticmethod
    def get_postgresql_options(
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_recycle: int = 3600,
        pool_timeout: int = 30,
        connect_timeout: int = 10,
        app_name: str = "gymnassic",
    ) -> dict[str, Any]:
        """
        Get recommended SQLAlchemy engine options for PostgreSQL.

        Args:
            pool_size: Number of connections to keep in pool
            max_overflow: Maximum overflow connections
            pool_recycle: Connection recycle time in seconds
            pool_timeout: Pool checkout timeout in seconds
            connect_timeout: Database connection timeout in seconds
            app_name: Application name for monitoring

        Returns:
            dict: PostgreSQL-specific engine options
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

    @staticmethod
    def get_mysql_options(
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_recycle: int = 3600,
        pool_timeout: int = 30,
        connect_timeout: int = 10,
    ) -> dict[str, Any]:
        """
        Get recommended SQLAlchemy engine options for MySQL.

        Args:
            pool_size: Number of connections to keep in pool
            max_overflow: Maximum overflow connections
            pool_recycle: Connection recycle time in seconds
            pool_timeout: Pool checkout timeout in seconds
            connect_timeout: Database connection timeout in seconds

        Returns:
            dict: MySQL-specific engine options
        """
        return {
            "pool_size": pool_size,
            "max_overflow": max_overflow,
            "pool_recycle": pool_recycle,
            "pool_pre_ping": True,
            "pool_timeout": pool_timeout,
            "connect_args": {
                "connect_timeout": connect_timeout,
            },
        }
