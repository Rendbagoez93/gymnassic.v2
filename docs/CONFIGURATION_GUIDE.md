# Configuration Guide

This document explains the configuration system for Gymnassic v2.

## Overview

The application uses **Pydantic Settings** for robust configuration management with:
- Type validation and coercion
- Environment-specific configurations
- .env file support
- Clear default values
- Comprehensive validation

## Configuration Files

### Structure

```
app/settings/
├── __init__.py          # Package exports
├── config.py            # Main configuration classes
└── containers.py        # Dependency injection containers
```

### Environment Files

Create environment-specific `.env` files:

- `.env.development` - Development settings
- `.env.production` - Production settings (required for deployment)
- `.env.testing` - Testing settings
- `.env` - Default fallback

**Examples are provided** in the project root:
- `.env.development.example`
- `.env.production.example`
- `.env.testing.example`

## Configuration Classes

### BaseConfig

Base configuration with sensible defaults for all environments.

**Key Settings:**
- Application info (name, version)
- Paths and uploads
- Database (SQLite by default)
- Security (sessions, CSRF, passwords)
- Email configuration
- Feature flags
- Logging

### DevelopmentConfig

Development-specific overrides:
- `DEBUG = True`
- `SQLALCHEMY_ECHO = True` (show SQL queries)
- `SESSION_COOKIE_SECURE = False` (allows HTTP)
- `MAIL_SUPPRESS_SEND = True` (don't send emails)
- `LOG_LEVEL = "DEBUG"`
- No static file caching

### ProductionConfig

Production-specific overrides:
- `DEBUG = False`
- PostgreSQL database (configurable)
- **ENFORCED security settings:**
  - `SESSION_COOKIE_SECURE = True` (HTTPS only)
  - `WTF_CSRF_ENABLED = True` (CSRF protection)
  - `SECRET_KEY` required (no default)
- Redis for rate limiting
- File logging enabled
- Long static file caching (1 year)
- Online payments enabled

### TestingConfig

Testing-specific overrides:
- In-memory SQLite database
- CSRF disabled
- Rate limiting disabled
- Relaxed password requirements (length = 4)

## Usage

### In Application Code

```python
from app import create_app

# Create app with default environment (from FLASK_ENV)
app = create_app()

# Create app with specific environment
app = create_app("development")
app = create_app("production")
app = create_app("testing")
```

### Getting Configuration Values

```python
from flask import current_app

# Access config in views
secret = current_app.config["SECRET_KEY"]
db_uri = current_app.config["SQLALCHEMY_DATABASE_URI"]
```

### With Dependency Injection

```python
from app.settings import ApplicationContainer

# Create container
container = ApplicationContainer()

# Get config
config = container.config()

# Access settings
print(config.APP_NAME)
print(config.DATABASE_URL)
```

## Environment Variables

All configuration values can be overridden with environment variables.

### Required in Production

```bash
SECRET_KEY=your-secure-random-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### Common Variables

```bash
# Flask
FLASK_ENV=development
DEBUG=true

# Database
DATABASE_URL=sqlite:///instance/gymnassic.db
SQLALCHEMY_ECHO=false

# Security
SECRET_KEY=your-secret-key
SESSION_COOKIE_SECURE=false
WTF_CSRF_ENABLED=true

# Email
MAIL_SERVER=localhost
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-password
MAIL_SUPPRESS_SEND=true

# Features
FEATURE_ONLINE_PAYMENT=false
FEATURE_EMAIL_NOTIFICATIONS=true
```

## Testing

### Run Configuration Tests

```bash
# All tests
uv run pytest tests/test_config.py -v

# Specific test class
uv run pytest tests/test_config.py::TestBaseConfig -v

# With coverage
uv run pytest tests/test_config.py --cov=app/settings
```

### Test Configuration in Code

```python
from app.settings import BaseConfig, DevelopmentConfig

# Test with custom values
config = DevelopmentConfig(
    DEBUG=False,
    DATABASE_URL="sqlite:///:memory:"
)

# Test without loading .env file
config = BaseConfig(_env_file=None)
```

## Validation

Pydantic automatically validates configuration:

### Type Validation

```python
# ✓ Valid
MAIL_PORT=587  # Converted to int

# ✗ Invalid
MAIL_PORT=abc  # ValidationError
```

### Boolean Parsing

Accepts multiple formats:
- `true`, `True`, `1`, `yes`, `on` → `True`
- `false`, `False`, `0`, `no`, `off` → `False`

### Custom Validation

Secret key validation in production:

```python
@field_validator("SECRET_KEY")
@classmethod
def validate_secret_key(cls, v: str, info) -> str:
    if info.data.get("ENV") == Environment.PRODUCTION:
        if v == "dev-secret-key-change-in-production":
            raise ValueError("SECRET_KEY must be set in production")
    return v
```

## Database Configuration

### SQLite (Development)

```bash
DATABASE_URL=sqlite:///instance/gymnassic.db
```

### PostgreSQL (Production)

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# Connection pool settings
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_RECYCLE=3600
DB_POOL_TIMEOUT=30
```

## Security Best Practices

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Production Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Configure PostgreSQL database
- [ ] Set `SESSION_COOKIE_SECURE=true`
- [ ] Configure SMTP for emails
- [ ] Set up Redis for rate limiting
- [ ] Enable file logging
- [ ] Review feature flags
- [ ] Test with production config before deployment

## Feature Flags

Control features via environment variables:

```bash
FEATURE_ONLINE_PAYMENT=true      # Enable/disable online payments
FEATURE_EMAIL_NOTIFICATIONS=true # Enable/disable email notifications
FEATURE_SMS_NOTIFICATIONS=false  # Enable/disable SMS notifications
```

## Troubleshooting

### ValidationError on Startup

Check environment variables match expected types:

```bash
# View current config
uv run python -c "from app.settings import get_config; config = get_config(); print(config.model_dump())"
```

### .env File Not Loading

Ensure file name matches environment:
- Development: `.env.development`
- Production: `.env.production`
- Testing: `.env.testing`
- Default: `.env`

### Database Connection Issues

Verify `DATABASE_URL` format:

```bash
# SQLite
sqlite:///path/to/database.db

# PostgreSQL
postgresql://username:password@host:port/database
```

## Migration from python-dotenv

The configuration has been migrated from `python-dotenv` to `pydantic-settings`:

**Old:**
```python
from dotenv import load_dotenv
SECRET_KEY = os.getenv("SECRET_KEY", "default")
```

**New:**
```python
from pydantic_settings import BaseSettings
class Config(BaseSettings):
    SECRET_KEY: str = "default"
```

**Benefits:**
- Type validation
- Better IDE support
- Automatic type conversion
- Validation errors on startup
- No need for manual `load_dotenv()`

## Additional Resources

- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Flask Configuration](https://flask.palletsprojects.com/en/latest/config/)
- [Dependency Injector](https://python-dependency-injector.ets-labs.org/)
