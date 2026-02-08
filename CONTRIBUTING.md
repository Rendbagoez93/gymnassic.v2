# Contributing to Gymnassic v2

Thank you for your interest in contributing to Gymnassic! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

### Prerequisites

- Python 3.13+
- UV package manager (recommended) or pip
- Git

### Setup Development Environment

1. **Fork and clone the repository**

```bash
git clone https://github.com/your-username/gymnassic.v2.git
cd gymnassic.v2
```

2. **Create a virtual environment and install dependencies**

```bash
# Using UV (recommended)
uv sync

# Or using pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install -e .
```

3. **Copy environment file**

```bash
cp .env.development.example .env.development
```

4. **Run tests to ensure everything works**

```bash
pytest
```

## Development Workflow

1. **Create a feature branch**

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

2. **Make your changes**
   - Write your code
   - Add tests for new functionality
   - Update documentation if needed

3. **Run code quality checks**

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy app/

# Run tests
pytest --cov=app
```

4. **Commit your changes**

```bash
git add .
git commit -m "feat: add new feature"
```

5. **Push to your fork**

```bash
git push origin feature/your-feature-name
```

6. **Create a Pull Request**

## Coding Standards

### Python Style Guide

- Follow **PEP 8** style guide
- Use **type hints** for function parameters and return values
- Maximum line length: **100 characters**
- Use **docstrings** for modules, classes, and functions

### Code Formatting

We use **Black** for code formatting and **Ruff** for linting:

```bash
# Auto-format all code
black .

# Check for linting issues
ruff check .

# Auto-fix linting issues
ruff check . --fix
```

### Type Checking

We use **MyPy** for static type checking:

```bash
mypy app/
```

### Directory Structure

- `app/` - Main application code
  - `settings/` - Configuration management
  - `auth/` - Authentication module
  - `core/` - Core pages and utilities
  - `extensions.py` - Flask extensions registry
- `tests/` - Test files
- `docs/` - Documentation

### Naming Conventions

- **Functions/methods**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private functions/methods**: `_leading_underscore`

## Testing

### Writing Tests

- Place tests in the `tests/` directory
- Name test files: `test_<module_name>.py`
- Name test functions: `test_<what_it_tests>`
- Use descriptive test names and docstrings

### Test Structure

```python
class TestFeatureName:
    """Test specific feature."""

    def test_specific_behavior(self):
        """Test that specific behavior works correctly."""
        # Arrange
        input_data = "test"
        
        # Act
        result = function_under_test(input_data)
        
        # Assert
        assert result == expected_output
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_config.py

# Run specific test
pytest tests/test_config.py::TestBaseConfig::test_base_config_defaults

# Run with verbose output
pytest -v
```

## Commit Messages

We follow the **Conventional Commits** specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring (no functional changes)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build, etc.)

### Examples

```bash
# Feature
git commit -m "feat(auth): add password reset functionality"

# Bug fix
git commit -m "fix(database): resolve connection pool timeout"

# Documentation
git commit -m "docs(readme): update installation instructions"

# Test
git commit -m "test(config): add tests for production config validation"
```

## Pull Request Process

1. **Ensure all tests pass**

```bash
pytest --cov=app
```

2. **Update documentation** if you've changed functionality

3. **Create a Pull Request** with:
   - Clear title describing the change
   - Detailed description of what changed and why
   - Reference any related issues (#123)
   - Screenshots for UI changes (if applicable)

4. **Code Review**
   - Address reviewer feedback
   - Keep commits clean and organized
   - Update your PR branch with main if needed

5. **Merge Requirements**
   - All tests passing ✅
   - Code review approved ✅
   - No merge conflicts ✅
   - Documentation updated ✅

## Project-Specific Guidelines

### Configuration Management

- Never hardcode configuration values
- Use `app/settings/config.py` for all configuration
- Add environment variables to `.env.*.example` files
- Document new configuration options in `docs/CONFIGURATION.md`

### Database Changes

- Create migrations for schema changes:
  ```bash
  flask db migrate -m "description of change"
  ```
- Test migrations both up and down
- Never modify existing migrations

### Security

- Never commit secrets or credentials
- Use environment variables for sensitive data
- Follow security best practices
- Report security issues privately

## Questions or Need Help?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas
- Check existing issues and discussions first

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing to Gymnassic! 🏋️**
