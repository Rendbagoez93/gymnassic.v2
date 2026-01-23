"""
Database Configuration Module

Manages database connection settings for SQLAlchemy.
Supports SQLite3 for Local/Development and PostgreSQL for Production.
"""

from .envcommon import get_env, get_bool_env, get_int_env, BASE_DIR


class DatabaseConfig:
    """Base Database Configuration"""
    
    # Common SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = get_bool_env(
        "SQLALCHEMY_TRACK_MODIFICATIONS",
        False
    )
    
    SQLALCHEMY_ECHO = get_bool_env("SQLALCHEMY_ECHO", False)
    
    # Default database URI (can be overridden by environment variable)
    SQLALCHEMY_DATABASE_URI = get_env(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'instance' / 'gymnassic.db'}"
    )
    
    # Default engine options (can be overridden)
    SQLALCHEMY_ENGINE_OPTIONS = {}


class SQLiteDatabaseConfig(DatabaseConfig):
    # SQLite3 Database (stored in instance/ directory)
    SQLALCHEMY_DATABASE_URI = get_env(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'instance' / 'gymnassic.db'}"
    )
    
    # SQLite-specific Engine Options (Default Values)
    # Note: SQLite has different pooling behavior than server databases
    SQLALCHEMY_ENGINE_OPTIONS = {
        # SQLite uses NullPool by default for file-based databases
        # This is appropriate for development
        "pool_pre_ping": get_bool_env("DB_POOL_PRE_PING", True),
        
        # SQLite specific: Enable foreign key support
        "connect_args": {
            "check_same_thread": False,  # Allow SQLite to be used across threads
        },
        
        # Echo SQL queries in development (can be overridden)
        "echo": get_bool_env("SQLALCHEMY_ECHO", False),
    }


class PostgresDatabaseConfig(DatabaseConfig):
    # PostgreSQL Database URI
    # Format: postgresql://username:password@host:port/database
    # Example: postgresql://gymnassic_user:password@localhost:5432/gymnassic_db
    SQLALCHEMY_DATABASE_URI = get_env(
        "DATABASE_URL",
        default="postgresql://localhost:5432/gymnassic_db"
    )
    
    # PostgreSQL Engine Options (Default Values - Adjustable)
    SQLALCHEMY_ENGINE_OPTIONS = {
        # Connection Pool Size
        # Number of connections to keep open in the pool
        "pool_size": get_int_env("DB_POOL_SIZE", 10),
        
        # Maximum Overflow
        # Maximum number of connections that can be created beyond pool_size
        "max_overflow": get_int_env("DB_MAX_OVERFLOW", 20),
        
        # Pool Recycle Time (seconds)
        # Recycle connections after this many seconds to prevent stale connections
        "pool_recycle": get_int_env("DB_POOL_RECYCLE", 3600),  # 1 hour
        
        # Pool Pre-Ping
        # Test connections before using them to ensure they're still valid
        "pool_pre_ping": get_bool_env("DB_POOL_PRE_PING", True),
        
        # Pool Timeout (seconds)
        # How long to wait for a connection from the pool
        "pool_timeout": get_int_env("DB_POOL_TIMEOUT", 30),
        
        # Echo SQL queries (typically False in production)
        "echo": get_bool_env("SQLALCHEMY_ECHO", False),
        
        # PostgreSQL-specific connection arguments
        "connect_args": {
            # Connection timeout
            "connect_timeout": get_int_env("DB_CONNECT_TIMEOUT", 10),
            
            # Application name (useful for monitoring)
            "application_name": get_env("DB_APP_NAME", "gymnassic"),
        },
    }
