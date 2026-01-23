# Configuration Setup Guide

## Overview

This document explains the configuration system for Gymnassic v2 application. The configuration is organized into modular files for better maintainability and security.

## Configuration Structure

```
app/settings/
├── __init__.py          # Package exports
├── base.py              # Main configuration classes (CENTRAL CONTROL PANEL)
├── envcommon.py         # Environment loading and utilities
├── security.py          # Security-related settings
└── databases.py         # Database configuration
```

## Environment Files

The application uses `.env` files to manage environment-specific settings:

- **`.env.development`** - Local development environment
- **`.env.production`** - Production environment
- **`.env.example`** - Template with all available options

### Setting Up Your Environment

1. **For Development:**
   ```bash
   # The .env.development file is already configured for local development
   # You can start developing immediately!
   ```

2. **For Production:**
   ```bash
   # Copy and customize the production environment file
   cp .env.production .env.production.local
   
   # Update the following CRITICAL values:
   # - SECRET_KEY (generate a secure random key)
   # - DATABASE_URL (your production database)
   # - MAIL_* settings (your SMTP credentials)
   ```

3. **Generate a Secure SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

## Configuration Classes

### BaseConfig
The foundation class that all environment configurations inherit from. Contains:
- Application metadata
- Common Flask settings
- Upload configuration
- Email settings
- Logging configuration
- Membership-specific settings
- Feature flags

### DevelopmentConfig
**Used for: Local development**

Key features:
- `DEBUG = True` - Enables debug mode
- `SQLALCHEMY_ECHO = True` - Shows SQL queries
- `SESSION_COOKIE_SECURE = False` - Allows HTTP
- `MAIL_SUPPRESS_SEND = True` - Doesn't send real emails
- Verbose logging (`LOG_LEVEL = DEBUG`)

### ProductionConfig
**Used for: Production deployment**

Key features:
- `DEBUG = False` - Debug mode disabled
- Enhanced security settings
- `SESSION_COOKIE_SECURE = True` - HTTPS only
- `SECRET_KEY` - **REQUIRED** from environment
- File logging with rotation
- Optimized database connections

### TestingConfig
**Used for: Automated testing**

Key features:
- In-memory SQLite database
- CSRF protection disabled
- Rate limiting disabled
- Fast password hashing

## Environment Variables

### Core Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Environment type | `development` | No |
| `SECRET_KEY` | Secret key for sessions | - | **Yes (Production)** |
| `DATABASE_URL` | Database connection string | SQLite path | No |

### Security Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `SESSION_COOKIE_SECURE` | HTTPS-only cookies | `false` |
| `WTF_CSRF_ENABLED` | CSRF protection | `true` |
| `PASSWORD_MIN_LENGTH` | Minimum password length | `8` |
| `RATELIMIT_ENABLED` | Enable rate limiting | `true` |

### Database Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `SQLALCHEMY_ECHO` | Log SQL queries | `false` |
| `DB_POOL_SIZE` | Connection pool size | `10` |
| `DB_POOL_RECYCLE` | Connection recycle time | `3600` |

### Email Settings

| Variable | Description | Required |
|----------|-------------|----------|
| `MAIL_SERVER` | SMTP server | No |
| `MAIL_PORT` | SMTP port | No |
| `MAIL_USERNAME` | SMTP username | No |
| `MAIL_PASSWORD` | SMTP password | No |
| `MAIL_SUPPRESS_SEND` | Disable email sending | No |

### Application Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `ITEMS_PER_PAGE` | Pagination items | `20` |
| `MEMBERSHIP_GRACE_PERIOD_DAYS` | Grace period | `3` |
| `PAYMENT_DUE_REMINDER_DAYS` | Payment reminder | `7` |

## Usage in Application

### Method 1: In run.py or app factory

```python
from app.settings import get_config
import os

# Get configuration based on FLASK_ENV
config_class = get_config()

# Or specify environment explicitly
config_class = get_config('production')

# Use with Flask
app.config.from_object(config_class)

# Initialize environment-specific settings
config_class.init_app(app)
```

### Method 2: Direct import

```python
from app.settings import DevelopmentConfig, ProductionConfig

# Use specific config
app.config.from_object(DevelopmentConfig)
```

### Method 3: Using environment utilities

```python
from app.settings import get_env, get_bool_env, get_int_env

# Get environment variables with type conversion
api_key = get_env('API_KEY', required=True)
debug_mode = get_bool_env('DEBUG', default=False)
max_items = get_int_env('MAX_ITEMS', default=100)
```

## Switching Environments

### Using Environment Variable
```bash
# Windows (PowerShell)
$env:FLASK_ENV="production"
python run.py

# Linux/Mac
export FLASK_ENV=production
python run.py
```

### Using .env Files
The system automatically loads the appropriate `.env` file based on `FLASK_ENV`:
- `FLASK_ENV=development` → loads `.env.development`
- `FLASK_ENV=production` → loads `.env.production`
- Not set → loads `.env` (fallback)

## Security Best Practices

### ✅ DO:
- Generate a strong, random `SECRET_KEY` for production
- Use environment variables for sensitive data
- Keep `.env` files out of version control
- Use HTTPS in production (`SESSION_COOKIE_SECURE=true`)
- Enable CSRF protection in production
- Use PostgreSQL or MySQL for production (not SQLite)
- Set up proper logging and monitoring

### ❌ DON'T:
- Commit `.env` files to Git
- Use default/development `SECRET_KEY` in production
- Expose debug mode in production
- Use SQLite in production with high traffic
- Disable security features without understanding implications

## Database Setup

### Development (SQLite)
```bash
# Already configured in .env.development
DATABASE_URL=sqlite:///instance/gymnassic.db
```

### Production (PostgreSQL)
```bash
# Update in .env.production
DATABASE_URL=postgresql://username:password@localhost:5432/gymnassic_db

# Create database
createdb gymnassic_db

# Run migrations
flask db upgrade
```

## Feature Flags

Control application features via environment variables:

- `FEATURE_ONLINE_PAYMENT` - Enable online payment processing
- `FEATURE_EMAIL_NOTIFICATIONS` - Enable email notifications
- `FEATURE_SMS_NOTIFICATIONS` - Enable SMS notifications

Example:
```bash
# .env.production
FEATURE_ONLINE_PAYMENT=true
FEATURE_EMAIL_NOTIFICATIONS=true
FEATURE_SMS_NOTIFICATIONS=false
```

## Troubleshooting

### "SECRET_KEY is required" Error
- Set `SECRET_KEY` in your environment file
- Generate one: `python -c "import secrets; print(secrets.token_hex(32))"`

### Database Connection Errors
- Check `DATABASE_URL` format
- Verify database server is running
- Ensure credentials are correct

### Email Not Sending
- Check SMTP settings in environment file
- Verify `MAIL_SUPPRESS_SEND=false` in production
- Test SMTP credentials

### Environment File Not Loading
- Check `FLASK_ENV` variable is set correctly
- Verify environment file exists in project root
- Check file permissions

## Adding New Configuration

1. **For general settings**: Add to `BaseConfig` in `base.py`
2. **For security settings**: Add to `SecurityConfig` in `security.py`
3. **For database settings**: Add to `DatabaseConfig` in `databases.py`
4. **For environment variables**: Use helper functions in `envcommon.py`

Example:
```python
# In security.py
class SecurityConfig:
    # Add new security setting
    NEW_SECURITY_FEATURE = get_bool_env('NEW_SECURITY_FEATURE', True)
```

## Related Documentation

- [Flask Configuration Documentation](https://flask.palletsprojects.com/en/latest/config/)
- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
- [SQLAlchemy Configuration](https://flask-sqlalchemy.palletsprojects.com/en/latest/config/)
