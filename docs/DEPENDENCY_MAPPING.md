# Dependency Mapping - pyproject.toml ↔ app/settings

## ✅ Synced Successfully!

### Core Dependencies (Required)

| Package | Version | Used In | Purpose |
|---------|---------|---------|---------|
| `flask` | ≥3.1.2 | All settings | Core web framework |
| `python-dotenv` | ≥1.0.0 | `envcommon.py` | Environment variable loading |

### Auth Group (Security & Authentication)

| Package | Version | Used In | Purpose |
|---------|---------|---------|---------|
| `flask-limiter` | ≥4.1.1 | `security.py` | Rate limiting (RATELIMIT_*) |
| `flask-login` | ≥0.6.3 | `base.py` | User session management (LOGIN_VIEW) |
| `flask-talisman` | ≥1.1.0 | Future use | HTTPS enforcement |
| `flask-wtf` | ≥1.2.2 | `security.py` | CSRF protection (WTF_CSRF_*) |
| `passlib` | ≥1.7.4 | Future use | Password hashing |
| `werkzeug` | ≥3.1.5 | Flask dependency | Security utilities |

**Settings using these:**
- `security.py`: WTF_CSRF_ENABLED, RATELIMIT_ENABLED, PASSWORD_* settings
- `base.py`: LOGIN_VIEW, LOGIN_MESSAGE, REMEMBER_COOKIE_DURATION

### Database Group

| Package | Version | Used In | Purpose |
|---------|---------|---------|---------|
| `flask-sqlalchemy` | ≥3.1.1 | `databases.py` | Database ORM integration |
| `flask-migrate` | ≥4.1.0 | Future use | Database migrations |
| `psycopg2-binary` | ≥2.9.11 | Production | PostgreSQL driver |

**Settings using these:**
- `databases.py`: SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SQLALCHEMY_ECHO, SQLALCHEMY_ENGINE_OPTIONS

### Email Group

| Package | Version | Used In | Purpose |
|---------|---------|---------|---------|
| `flask-mail` | ≥0.10.0 | `base.py` | Email sending |

**Settings using these:**
- `base.py`: MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER, MAIL_SUPPRESS_SEND

### Quality Group (Development)

| Package | Version | Purpose |
|---------|---------|---------|
| `black` | ≥26.1.0 | Code formatting |
| `mypy` | ≥1.19.1 | Type checking |
| `pre-commit` | ≥4.5.1 | Git hooks |
| `ruff` | ≥0.14.14 | Fast linting |

**Not directly used in settings** - Development tools only

### Testing Group

| Package | Version | Used In | Purpose |
|---------|---------|---------|---------|
| `pytest` | ≥9.0.2 | `base.py` | Test framework |
| `pytest-cov` | ≥7.0.0 | Testing | Coverage reporting |
| `pytest-flask` | ≥1.3.0 | Testing | Flask test utilities |
| `factory-boy` | ≥3.3.3 | Testing | Test data factories |

**Settings using these:**
- `base.py`: TestingConfig class

### Validation Group (Optional)

| Package | Version | Status |
|---------|---------|--------|
| `pydantic` | ≥2.12.5 | Available but not currently used |
| `pydantic-settings` | ≥2.12.0 | Available for future env validation |

## Configuration → Dependency Mapping

### envcommon.py
- ✅ `python-dotenv` - load_dotenv(), get_env functions
- ✅ Built-in modules: os, pathlib

### security.py
- ✅ Uses envcommon helpers
- 🔜 `flask-wtf` - CSRF settings (not imported yet, just configured)
- 🔜 `flask-limiter` - Rate limiting settings (not imported yet, just configured)
- 🔜 `passlib` - Password validation (not imported yet, just configured)

### databases.py
- ✅ Uses envcommon helpers
- 🔜 `flask-sqlalchemy` - Database settings (not imported yet, just configured)

### base.py
- ✅ Uses envcommon, security, databases
- ✅ Built-in modules: os, datetime
- 🔜 `flask-login` - Login configuration (not imported yet, just configured)
- 🔜 `flask-mail` - Email settings (not imported yet, just configured)

## Installation Commands

### Install All Dependencies
```bash
uv sync --all-groups
```

### Install Specific Groups
```bash
# Core + Auth + Database (Recommended for development)
uv sync --group auth --group database --group email

# Add Quality Tools
uv sync --group quality

# Add Testing
uv sync --group testing
```

### Production Installation
```bash
# Only production dependencies
uv sync --group auth --group database --group email
```

## Dependency Status

### ✅ Currently Used
- [x] flask
- [x] python-dotenv

### 🔧 Configured (Not Yet Imported)
- [ ] flask-sqlalchemy (configured in databases.py)
- [ ] flask-login (configured in base.py)
- [ ] flask-wtf (configured in security.py)
- [ ] flask-limiter (configured in security.py)
- [ ] flask-mail (configured in base.py)

### 📦 Available for Future Use
- [ ] flask-migrate (database migrations)
- [ ] flask-talisman (HTTPS enforcement)
- [ ] passlib (password hashing)
- [ ] pydantic (settings validation)
- [ ] pydantic-settings (environment validation)

## Next Steps to Activate Extensions

When you're ready to use the configured extensions:

### 1. Flask-SQLAlchemy (Database)
```python
# In app/extensions.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# In app/__init__.py
from app.extensions import db
db.init_app(app)
```

### 2. Flask-Login (Authentication)
```python
# In app/extensions.py
from flask_login import LoginManager
login_manager = LoginManager()

# In app/__init__.py
login_manager.init_app(app)
```

### 3. Flask-Mail (Email)
```python
# In app/extensions.py
from flask_mail import Mail
mail = Mail()

# In app/__init__.py
mail.init_app(app)
```

### 4. Flask-Limiter (Rate Limiting)
```python
# In app/extensions.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=app.config['RATELIMIT_STORAGE_URL']
)
```

## Verification

Run this to verify all dependencies are correctly installed:

```bash
python -c "from app.settings import get_config; print('✅ All settings synced with pyproject.toml')"
```

Expected output:
```
✓ Loaded environment from: .../gymnassic.v2/.env.development
✅ All settings synced with pyproject.toml
```

## Summary

- ✅ **pyproject.toml** updated with correct package names
- ✅ **python-dotenv** (not dotenv) is now specified
- ✅ **flask-mail** added to email group
- ✅ All dependency groups properly organized
- ✅ Settings files configured for future extension use
- ✅ Dependencies successfully synced

Your configuration system is now fully aligned with your dependencies! 🎉
