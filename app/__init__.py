"""
Gymnassic v2 - Gym Membership Management Application

A Flask-based application for managing gym memberships, member sign-ups,
logins, membership packages, payment tracking, and due dates.
"""

from flask import Flask
from app.settings import get_config


def create_app(config_name=None):
    """
    Application Factory Pattern
    
    Creates and configures the Flask application instance.
    
    Args:
        config_name: Configuration environment name ('development', 'production', 'testing')
                    If None, uses FLASK_ENV environment variable
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    config_instance = get_config(config_name)
    
    # Convert Pydantic settings to dict and load into Flask
    config_dict = config_instance.model_dump()
    for key, value in config_dict.items():
        app.config[key.upper()] = value
    
    # Add computed properties
    app.config['SQLALCHEMY_DATABASE_URI'] = config_instance.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = config_instance.SQLALCHEMY_ENGINE_OPTIONS
    
    # Initialize configuration-specific setup
    config_instance.__class__.init_app(app)
    
    # Initialize extensions
    from app.extensions import init_extensions
    init_extensions(app)
    
    # Register blueprints (to be implemented)
    # register_blueprints(app)
    
    # Register error handlers (to be implemented)
    # register_error_handlers(app)
    
    # Context processors (to be implemented)
    # register_context_processors(app)
    
    return app


def initialize_extensions(app):
    """
    Initialize Flask extensions
    
    This will include:
    - SQLAlchemy (database)
    - Flask-Login (authentication)
    - Flask-Migrate (database migrations)
    - Flask-WTF (forms)
    - Flask-Limiter (rate limiting)
    - etc.
    """
    # from app.extensions import db, migrate, login_manager, limiter
    # db.init_app(app)
    # migrate.init_app(app, db)
    # login_manager.init_app(app)
    # limiter.init_app(app)
    pass


def register_blueprints(app):
    """
    Register Flask blueprints
    
    Blueprints organize the application into modular components:
    - auth: Authentication (login, signup, logout)
    - members: Member management
    - subscriptions: Membership packages
    - payments: Payment tracking
    - core: Core pages (home, dashboard)
    """
    # from auth.routes import auth_bp
    # from members.routes import members_bp
    # from subscriptions.routes import subscriptions_bp
    # from payments.routes import payments_bp
    # from core.routes import core_bp
    
    # app.register_blueprint(core_bp)
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(members_bp, url_prefix='/members')
    # app.register_blueprint(subscriptions_bp, url_prefix='/subscriptions')
    # app.register_blueprint(payments_bp, url_prefix='/payments')
    pass


def register_error_handlers(app):
    """Register error handlers for common HTTP errors"""
    # @app.errorhandler(404)
    # def not_found_error(error):
    #     return render_template('errors/404.html'), 404
    
    # @app.errorhandler(500)
    # def internal_error(error):
    #     return render_template('errors/500.html'), 500
    pass


def register_context_processors(app):
    """Register context processors for templates"""
    # @app.context_processor
    # def utility_processor():
    #     return {
    #         'app_name': app.config['APP_NAME'],
    #         'app_version': app.config['APP_VERSION'],
    #     }
    pass
