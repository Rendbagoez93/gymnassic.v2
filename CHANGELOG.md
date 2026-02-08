# Changelog

All notable changes to the Gymnassic v2 project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
- Modular configuration system with Pydantic Settings
- Environment-specific configurations (Development, Production, Testing)
- Dependency injection with dependency-injector
- Comprehensive test suite
- Flask extensions registry
- Gym profile configuration system
- Security utilities (password validation, CSRF, rate limiting)
- Database utilities and migration support
- Documentation structure

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [2.0.0] - 2026-02-08

### Added
- **Configuration Management**
  - Centralized configuration in `app/settings/`
  - Pydantic-based settings with validation
  - Environment-specific configs (development, production, testing)
  - Gym profile configuration with JSON schema validation
  - `.env` file support for all environments

- **Application Infrastructure**
  - Flask application factory pattern
  - Flask extensions registry
  - Dependency injection container
  - Comprehensive error handling framework (prepared)

- **Database**
  - SQLAlchemy integration
  - Flask-Migrate for database migrations
  - Support for SQLite (development) and PostgreSQL (production)
  - Connection pooling configuration

- **Security**
  - Flask-Login for authentication
  - CSRF protection with Flask-WTF
  - Rate limiting with Flask-Limiter
  - HTTPS security headers with Flask-Talisman
  - Password hashing with bcrypt
  - Password strength validation

- **Testing**
  - Pytest test suite
  - Test fixtures and configuration
  - Code coverage reporting
  - Tests for all configuration modules
  - Tests for database utilities
  - Tests for security utilities
  - Tests for environment management
  - Tests for gym configuration
  - Tests for extensions

- **Development Tools**
  - Black for code formatting
  - Ruff for linting
  - MyPy for type checking
  - Pre-commit hooks support
  - UV package manager support

- **Documentation**
  - Architecture documentation
  - Configuration guide
  - Setup guide
  - Quick reference
  - API documentation structure (prepared)
  - Contributing guidelines
  - README with comprehensive setup instructions

### Project Structure
```
gymnassic.v2/
├── app/
│   ├── settings/          # Configuration management
│   │   ├── config.py      # Main configuration classes
│   │   ├── containers.py  # Dependency injection
│   │   ├── databases.py   # Database utilities
│   │   ├── envcommon.py   # Environment utilities
│   │   ├── gymconf.py     # Gym profile configuration
│   │   ├── security.py    # Security utilities
│   │   └── __init__.py
│   ├── __init__.py        # Application factory
│   ├── extensions.py      # Flask extensions
│   ├── auth/              # Authentication (prepared)
│   ├── core/              # Core pages (prepared)
│   ├── members/           # Member management (prepared)
│   ├── payments/          # Payment processing (prepared)
│   └── subscriptions/     # Membership packages (prepared)
├── tests/                 # Comprehensive test suite
├── docs/                  # Documentation
├── pyproject.toml         # Dependencies and tools
├── run.py                 # Application entry point
└── README.md              # Project documentation
```

## Version Numbering

- **Major version** (X.0.0): Breaking changes
- **Minor version** (0.X.0): New features, backwards compatible
- **Patch version** (0.0.X): Bug fixes, backwards compatible

---

**Note**: This changelog will be updated with each release. For development changes not yet released, see the "Unreleased" section above.
