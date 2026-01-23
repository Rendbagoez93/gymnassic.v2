# Quick Reference - Configuration Setup

## File Structure
```
app/settings/
├── base.py         → CENTRAL CONTROL PANEL (all Flask configs)
├── envcommon.py    → Environment loading & utilities
├── security.py     → Security settings
└── databases.py    → Database configuration
```

## Environment Files
- `.env.development` → Local development (pre-configured ✅)
- `.env.production`  → Production (requires setup)
- `.env.example`     → Template with all options

## Quick Commands

### Start Development Server
```bash
python run.py
```

### Switch to Production
```bash
# Windows
$env:FLASK_ENV="production"

# Linux/Mac
export FLASK_ENV=production
```

### Generate Secret Key
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Configuration Classes

### BaseConfig
- Foundation for all configs
- Contains: app settings, uploads, email, logging, membership settings

### DevelopmentConfig
- Debug: ON
- Database: SQLite
- Security: Relaxed
- Email: Suppressed

### ProductionConfig  
- Debug: OFF
- Database: PostgreSQL recommended
- Security: Enhanced
- Email: Active
- Logging: File rotation

## Using Configuration

### In app factory (app/__init__.py)
```python
from app.settings import get_config

config_class = get_config()  # Auto-detects from FLASK_ENV
app.config.from_object(config_class)
config_class.init_app(app)
```

### Get environment variables
```python
from app.settings import get_env, get_bool_env, get_int_env

api_key = get_env('API_KEY', required=True)
debug = get_bool_env('DEBUG', default=False)
max_items = get_int_env('MAX_ITEMS', default=100)
```

## Critical Production Settings

Must update in `.env.production`:
- `SECRET_KEY` - Generate secure random key
- `DATABASE_URL` - PostgreSQL connection
- `MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD` - SMTP
- `SESSION_COOKIE_SECURE=true` - Requires HTTPS

## Common Environment Variables

| Variable | Dev Default | Production Default |
|----------|-------------|-------------------|
| `FLASK_ENV` | development | production |
| `DEBUG` | true | false |
| `DATABASE_URL` | SQLite | Must set PostgreSQL |
| `SECRET_KEY` | dev-key | **Required!** |
| `SQLALCHEMY_ECHO` | true | false |
| `LOG_LEVEL` | DEBUG | WARNING |

## Features Controlled by Config

Modify in `.env` files:
- `FEATURE_ONLINE_PAYMENT` - Payment processing
- `FEATURE_EMAIL_NOTIFICATIONS` - Email alerts
- `FEATURE_SMS_NOTIFICATIONS` - SMS alerts
- `MEMBERSHIP_GRACE_PERIOD_DAYS` - Payment grace period
- `PAYMENT_DUE_REMINDER_DAYS` - Reminder timing

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "SECRET_KEY required" | Set in .env file or generate new one |
| Database errors | Check DATABASE_URL format |
| Email not sending | Verify SMTP settings, check MAIL_SUPPRESS_SEND |
| Wrong environment | Set FLASK_ENV variable correctly |

## Full Documentation
See [docs/CONFIGURATION.md](../CONFIGURATION.md) for complete details.
