"""
Pytest Configuration and Shared Fixtures

This module provides common fixtures and configuration for all tests.
"""

import pytest

from app import create_app
from app.settings import Environment


@pytest.fixture(scope="session")
def app():
    """
    Create and configure a test application instance.

    Scope: session - created once per test session.
    """
    app = create_app(Environment.TESTING)

    # Create application context
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope="function")
def client(app):
    """
    Create a test client for the app.

    Scope: function - created for each test function.
    """
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """
    Create a test CLI runner for the app.

    Scope: function - created for each test function.
    """
    return app.test_cli_runner()
