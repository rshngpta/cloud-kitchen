"""
Cloud Kitchen - Application Configuration Module
================================================
Author: [Your Name]
Date: December 2025
Module: H9CDOS - Cloud DevOps

Description:
    This module contains configuration settings for the Flask application.
    It uses environment variables for sensitive data and provides defaults
    for development environments.

Configuration Approach:
    - Environment variables for production secrets
    - Fallback defaults for development
    - Conditional database path for AWS deployment

Security Best Practices:
    - SECRET_KEY should always be set via environment variable in production
    - Database credentials should never be hardcoded
    - Debug mode should be disabled in production
"""

# ==============================================================================
# IMPORTS
# ==============================================================================
import os  # Operating system interface for environment variables


# ==============================================================================
# CONFIGURATION CLASS
# ==============================================================================

class Config:
    """
    Application Configuration Class
    ================================
    
    Contains all configuration settings for the Flask application.
    Settings are loaded from environment variables with fallback defaults.
    
    Attributes:
        SECRET_KEY (str): Secret key for session encryption and CSRF tokens
        SQLALCHEMY_DATABASE_URI (str): Database connection string
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): SQLAlchemy event tracking
        WTF_CSRF_ENABLED (bool): Enable CSRF protection
    
    Environment Variables:
        SECRET_KEY: Override the default secret key
        DATABASE_URL: Override the database connection string
        AWS_EXECUTION_ENV: Set automatically by AWS Elastic Beanstalk
    
    Usage:
        app = Flask(__name__)
        app.config.from_object(Config)
    """
    
    # ==========================================================================
    # SECRET KEY CONFIGURATION
    # ==========================================================================
    
    # Secret key for cryptographic operations
    # Used for:
    #   - Session cookie signing
    #   - CSRF token generation
    #   - Flash message signing
    #
    # IMPORTANT: In production, always set SECRET_KEY environment variable
    # with a strong, random value. Generate with:
    #   python -c "import secrets; print(secrets.token_hex(32))"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cloud-kitchen-secret-key-2024'
    
    # ==========================================================================
    # DATABASE CONFIGURATION
    # ==========================================================================
    
    # Database URI configuration with AWS-aware path handling
    #
    # Problem: On AWS Elastic Beanstalk, the application directory is read-only,
    # so SQLite cannot write to the default location.
    #
    # Solution: Detect AWS environment and use /tmp directory which is writable.
    #
    # Note: /tmp is ephemeral on AWS - data is lost on instance restart.
    # For production, use AWS RDS (PostgreSQL/MySQL) instead of SQLite.
    
    if os.environ.get('AWS_EXECUTION_ENV'):
        # Running on AWS Elastic Beanstalk - use writable /tmp directory
        # AWS_EXECUTION_ENV is automatically set by Elastic Beanstalk
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/cloud_kitchen.db'
    else:
        # Local development - use instance folder or environment variable
        # DATABASE_URL environment variable takes precedence if set
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///cloud_kitchen.db'
    
    # ==========================================================================
    # SQLALCHEMY CONFIGURATION
    # ==========================================================================
    
    # Disable SQLAlchemy modification tracking
    # This feature is deprecated and adds overhead
    # Set to False to suppress warning and improve performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ==========================================================================
    # SECURITY CONFIGURATION
    # ==========================================================================
    
    # Enable CSRF (Cross-Site Request Forgery) protection
    # This adds a hidden token to forms that is validated on submission
    # Prevents malicious sites from submitting forms on behalf of users
    WTF_CSRF_ENABLED = True
