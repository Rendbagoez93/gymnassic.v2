"""
Gymnassic v2 - Application Entry Point

This script runs the Flask development server.
For production, use a WSGI server like Gunicorn or uWSGI.
"""

import os
from app import create_app

# Create Flask application
# Environment is automatically detected from FLASK_ENV environment variable
# Default: development
app = create_app()

if __name__ == '__main__':
    # Get host and port from environment or use defaults
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    # Run development server
    # WARNING: Never use this in production! Use Gunicorn, uWSGI, or similar
    app.run(
        host=host,
        port=port,
        debug=app.config.get('DEBUG', False)
    )
