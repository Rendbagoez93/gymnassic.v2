"""
Test Database Utilities Module

Tests for database utility functions.
"""

import pytest

from app.settings.databases import (
    ensure_instance_directory,
    get_postgresql_engine_options,
    get_postgresql_uri,
    get_sqlite_engine_options,
    get_sqlite_path,
)


class TestGetSqlitePath:
    """Test get_sqlite_path function."""

    def test_get_sqlite_path_default(self):
        """Test getting default SQLite path."""
        path = get_sqlite_path()
        assert path.startswith("sqlite:///")
        assert path.endswith("gymnassic.db")

    def test_get_sqlite_path_custom(self):
        """Test getting custom SQLite path."""
        path = get_sqlite_path("test.db")
        assert path.startswith("sqlite:///")
        assert path.endswith("test.db")


class TestGetPostgresqlUri:
    """Test get_postgresql_uri function."""

    def test_get_postgresql_uri_basic(self):
        """Test building basic PostgreSQL URI."""
        uri = get_postgresql_uri("user", "pass")
        assert uri == "postgresql://user:pass@localhost:5432/gymnassic_db"

    def test_get_postgresql_uri_custom_host(self):
        """Test PostgreSQL URI with custom host."""
        uri = get_postgresql_uri("user", "pass", host="db.example.com")
        assert uri == "postgresql://user:pass@db.example.com:5432/gymnassic_db"

    def test_get_postgresql_uri_custom_port(self):
        """Test PostgreSQL URI with custom port."""
        uri = get_postgresql_uri("user", "pass", port=5433)
        assert uri == "postgresql://user:pass@localhost:5433/gymnassic_db"

    def test_get_postgresql_uri_custom_database(self):
        """Test PostgreSQL URI with custom database."""
        uri = get_postgresql_uri("user", "pass", database="test_db")
        assert uri == "postgresql://user:pass@localhost:5432/test_db"

    def test_get_postgresql_uri_all_custom(self):
        """Test PostgreSQL URI with all custom parameters."""
        uri = get_postgresql_uri(
            username="admin",
            password="secret123",
            host="prod-db.example.com",
            port=5433,
            database="production_db",
        )
        expected = "postgresql://admin:secret123@prod-db.example.com:5433/production_db"
        assert uri == expected


class TestGetSqliteEngineOptions:
    """Test get_sqlite_engine_options function."""

    def test_get_sqlite_engine_options(self):
        """Test getting SQLite engine options."""
        options = get_sqlite_engine_options()

        assert isinstance(options, dict)
        assert "pool_pre_ping" in options
        assert "connect_args" in options
        assert options["pool_pre_ping"] is True
        assert options["connect_args"]["check_same_thread"] is False


class TestGetPostgresqlEngineOptions:
    """Test get_postgresql_engine_options function."""

    def test_get_postgresql_engine_options_defaults(self):
        """Test PostgreSQL engine options with defaults."""
        options = get_postgresql_engine_options()

        assert isinstance(options, dict)
        assert options["pool_size"] == 10
        assert options["max_overflow"] == 20
        assert options["pool_recycle"] == 3600
        assert options["pool_pre_ping"] is True
        assert options["pool_timeout"] == 30
        assert "connect_args" in options
        assert options["connect_args"]["connect_timeout"] == 10
        assert options["connect_args"]["application_name"] == "gymnassic"

    def test_get_postgresql_engine_options_custom(self):
        """Test PostgreSQL engine options with custom values."""
        options = get_postgresql_engine_options(
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


class TestEnsureInstanceDirectory:
    """Test ensure_instance_directory function."""

    def test_ensure_instance_directory(self):
        """Test ensuring instance directory exists."""
        instance_dir = ensure_instance_directory()

        assert instance_dir.exists()
        assert instance_dir.is_dir()
        assert instance_dir.name == "instance"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
