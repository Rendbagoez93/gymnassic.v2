# Gymnassic v2 🏋️

A modern Flask-based Gym Membership Management System that serves as a SignUp Gateway for gym subscriptions, managing member registrations, logins, membership packages, payments, and due dates.

## Features

- 👤 **Member Management**: Sign up and login system for gym members
- 📊 **Dashboard**: Personalized member dashboard showing:
  - Current membership package information
  - Membership due dates
  - Payment history and status
- 💳 **Payment Tracking**: Monitor and manage member payments
- 📦 **Subscription Packages**: Manage different membership tiers
- 🔒 **Security**: Built-in authentication, CSRF protection, and rate limiting
- 🌍 **Multi-Environment**: Separate configurations for development and production

## Tech Stack

- **Framework**: Flask 3.1+
- **Database**: SQLAlchemy (SQLite for dev, PostgreSQL for production)
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Migrations**: Flask-Migrate
- **Security**: Flask-Talisman, Rate Limiting
- **Configuration**: Pydantic Settings 2.12+
- **Dependency Injection**: dependency-injector 4.48+
- **Code Quality**: Black, Ruff, MyPy
- **Testing**: Pytest, Pytest-Cov

## Project Structure

```
gymnassic.v2/
├── app/
│   ├── settings/           # Configuration management (CENTRAL CONTROL)
│   │   ├── config.py      # Pydantic Settings classes
│   │   ├── containers.py  # Dependency injection
│   │   └── __init__.py    # Package exports
│   ├── __init__.py        # Application factory
│   └── extensions.py      # Flask extensions
├── auth/                  # Authentication module
├── members/              # Member management
├── subscriptions/        # Membership packages
├── payments/             # Payment processing
├── core/                 # Core pages
├── static/               # CSS, JS, images
├── templates/            # HTML templates
├── migrations/           # Database migrations
├── tests/                # Unit tests
├── docs/                 # Documentation
├── run.py               # Application entry point
└── pyproject.toml       # Dependencies & tool configs
```

## Quick Start

### 1. Prerequisites

- Python 3.13+
- UV package manager (recommended) or pip

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd gymnassic.v2

# Install dependencies using UV
uv sync

# Or using pip
pip install -e .
```

### 3. Configuration

The application is **pre-configured** for development! You can start immediately.

For custom settings:
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your preferred settings
# See docs/CONFIGURATION.md for all options
```

### 4. Run the Application

```bash
# Activate virtual environment (if using uv)
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\Activate.ps1  # Windows PowerShell

# Run development server
python run.py
```

Visit http://127.0.0.1:5000 in your browser.

## Configuration

The application uses a **modular configuration system** with two environments:

### Development Environment (Default)
- **File**: `.env.development`
- **Features**:
  - Debug mode enabled
  - SQLite database
  - Verbose logging
  - Email suppression
  - Relaxed security for testing

### Production Environment
- **File**: `.env.production`
- **Features**:
  - Debug mode disabled
  - PostgreSQL database (recommended)
  - Enhanced security
  - File logging
  - HTTPS-only sessions

### Switching Environments

```bash
# Windows (PowerShell)
$env:FLASK_ENV="production"
python run.py

# Linux/Mac
export FLASK_ENV=production
python run.py
```

### Key Configuration Files

- [`app/settings/base.py`](app/settings/base.py) - **Central Control Panel** for all Flask settings
- [`app/settings/envcommon.py`](app/settings/envcommon.py) - Environment loading and utilities
- [`app/settings/security.py`](app/settings/security.py) - Security settings
- [`app/settings/databases.py`](app/settings/databases.py) - Database configuration

📖 **Full documentation**: See [docs/CONFIGURATION.md](docs/CONFIGURATION.md)

## Environment Variables

Essential variables (with defaults):

```bash
# Environment
FLASK_ENV=development          # development, production, testing

# Security
SECRET_KEY=<random-key>        # Required for production!

# Database
DATABASE_URL=sqlite:///instance/gymnassic.db

# Email
MAIL_SERVER=localhost
MAIL_PORT=587
```

📋 See [`.env.example`](.env.example) for all available options.

## Database Setup

```bash
# Initialize migrations (first time)
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

## Development

### Code Quality Tools

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy app/

# Run all checks
pre-commit run --all-files
```

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## Production Deployment

### 1. Configure Production Environment

```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Update .env.production with:
# - SECRET_KEY (generated above)
# - DATABASE_URL (PostgreSQL connection)
# - MAIL_* settings (SMTP credentials)
# - Set FLASK_ENV=production
```

### 2. Use Production Server

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('production')"
```

### 3. Security Checklist

- ✅ Set strong `SECRET_KEY`
- ✅ Use PostgreSQL (not SQLite)
- ✅ Enable HTTPS
- ✅ Set `SESSION_COOKIE_SECURE=true`
- ✅ Configure proper SMTP settings
- ✅ Review all security settings in `.env.production`

## API Documentation

(To be added as features are implemented)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Your License Here]

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Made with ❤️ for gym management**
