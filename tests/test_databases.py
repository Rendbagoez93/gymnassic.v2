"""
Test Database Utilities Module

Tests for database utility functions.
"""

import pytest

from app.settings.databases import DatabaseConfig, DatabaseEngine


class TestDatabaseConfig:
    """Test DatabaseConfig class."""

    def test_detect_engine_sqlite(self):
        """Test detecting SQLite engine."""
        engine = DatabaseConfig.detect_engine("sqlite:///test.db")
        assert engine == DatabaseEngine.SQLITE

    def test_detect_engine_postgresql(self):
        """Test detecting PostgreSQL engine."""
        engine = DatabaseConfig.detect_engine("postgresql://user:pass@localhost/db")
        assert engine == DatabaseEngine.POSTGRESQL

    def test_detect_engine_postgres_variant(self):
        """Test detecting Postgres variant."""
        engine = DatabaseConfig.detect_engine("postgres://user:pass@localhost/db")
        assert engine == DatabaseEngine.POSTGRESQL

    def test_detect_engine_mysql(self):
        """Test detecting MySQL engine."""
        engine = DatabaseConfig.detect_engine("mysql://user:pass@localhost/db")
        assert engine == DatabaseEngine.MYSQL

    def test_get_sqlite_options(self):
        """Test getting SQLite engine options."""
        options = DatabaseConfig.get_sqlite_options()

        assert isinstance(options, dict)
        assert "pool_pre_ping" in options
        assert "connect_args" in options
        assert options["pool_pre_ping"] is True
        assert options["connect_args"]["check_same_thread"] is False

    def test_get_postgresql_options_defaults(self):
        """Test PostgreSQL engine options with defaults."""
        options = DatabaseConfig.get_postgresql_options()

        assert isinstance(options, dict)
        assert options["pool_size"] == 10
        assert options["max_overflow"] == 20
        assert options["pool_recycle"] == 3600
        assert options["pool_pre_ping"] is True
        assert options["pool_timeout"] == 30
        assert "connect_args" in options
        assert options["connect_args"]["connect_timeout"] == 10
        assert options["connect_args"]["application_name"] == "gymnassic"

    def test_get_postgresql_options_custom(self):
        """Test PostgreSQL engine options with custom values."""
        options = DatabaseConfig.get_postgresql_options(
            pool_size=20,
            max_overflow=40,
            pool_recycle=1800,
            pool_timeout=60,
            connect_timeout=20,
            app_name="test_app",
        )

        assert options["pool_size"] == 20
        assert options["max_overflow"] == 40
        assert options["pool_recycle"] == 1800
        assert options["pool_timeout"] == 60
        assert options["connect_args"]["connect_timeout"] == 20
        assert options["connect_args"]["application_name"] == "test_app"

    def test_get_mysql_options(self):
        """Test MySQL engine options."""
        options = DatabaseConfig.get_mysql_options()

        assert isinstance(options, dict)
        assert options["pool_size"] == 10
        assert options["max_overflow"] == 20
        assert options["pool_recycle"] == 3600
        assert options["pool_pre_ping"] is True
        assert options["pool_timeout"] == 30
        assert "connect_args" in options
        assert options["connect_args"]["connect_timeout"] == 10

    def test_get_engine_options_sqlite(self):
        """Test getting engine options for SQLite."""
        options = DatabaseConfig.get_engine_options("sqlite:///test.db")

        assert isinstance(options, dict)
        assert "pool_pre_ping" in options
        assert "connect_args" in options

    def test_get_engine_options_postgresql(self):
        """Test getting engine options for PostgreSQL."""
        options = DatabaseConfig.get_engine_options(
            "postgresql://user:pass@localhost/db",
            pool_size=15,
            app_name="test",
        )

        assert options["pool_size"] == 15
        assert options["connect_args"]["application_name"] == "test"

    def test_get_engine_options_mysql(self):
        """Test getting engine options for MySQL."""
        options = DatabaseConfig.get_engine_options(
            "mysql://user:pass@localhost/db", pool_size=25
        )

        assert options["pool_size"] == 25


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
