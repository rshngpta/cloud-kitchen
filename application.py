"""
Cloud Kitchen - AWS Elastic Beanstalk Entry Point
==================================================
Author: [Your Name]
Date: December 2025
Module: H9CDOS - Cloud DevOps

Description:
    This module serves as the entry point for AWS Elastic Beanstalk deployment.
    Elastic Beanstalk expects an 'application' callable by default, so this
    file imports the Flask app and exposes it with the correct name.

AWS Elastic Beanstalk Requirements:
    - Application must be named 'application' (not 'app')
    - This file must be in the root directory
    - Procfile specifies how to run: "web: gunicorn application:application"

Why This File Exists:
    Flask applications typically use 'app' as the variable name, but
    AWS Elastic Beanstalk looks for 'application'. This wrapper module
    bridges that naming convention without modifying the main app.py file.

Usage:
    This file is automatically used by:
    - AWS Elastic Beanstalk (via Procfile)
    - Gunicorn WSGI server

Local Development:
    Can also be run directly for local testing:
    $ python application.py
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

# Import the Flask application instance from main app module
# 'app' is renamed to 'application' to match AWS EB's expected name
from app import app as application


# ==============================================================================
# LOCAL DEVELOPMENT ENTRY POINT
# ==============================================================================

if __name__ == '__main__':
    """
    Development Server
    ------------------
    This block runs when the script is executed directly.
    It starts Flask's built-in development server.
    
    Note: Do not use this in production. Use Gunicorn instead:
        gunicorn application:application
    
    The development server is for testing only and lacks:
        - Multi-threaded request handling
        - Production-grade security
        - Process management
    """
    # Run Flask development server
    # debug=True enables auto-reload and detailed error pages
    application.run(debug=True)
