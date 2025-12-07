import os

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cloud-kitchen-secret-key-2024'
    
    # Use /tmp for SQLite on AWS (writable location)
    if os.environ.get('AWS_EXECUTION_ENV'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/cloud_kitchen.db'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///cloud_kitchen.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

