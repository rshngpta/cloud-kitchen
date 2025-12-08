# ==============================================================================
# Cloud Kitchen - Docker Configuration
# ==============================================================================
# Author: [Your Name]
# Date: December 2025
# Module: H9CDOS - Cloud DevOps
#
# Description:
#     This Dockerfile defines the container image for the Cloud Kitchen
#     Flask application. It follows Docker best practices for Python
#     applications including multi-stage awareness, security hardening,
#     and health checking.
#
# Build Command:
#     docker build -t cloud-kitchen .
#
# Run Command:
#     docker run -p 5000:5000 cloud-kitchen
#
# Docker Compose:
#     docker compose up --build
# ==============================================================================

# ==============================================================================
# BASE IMAGE
# ==============================================================================
# Using Python 3.11 slim variant for smaller image size
# Slim images include minimal packages needed to run Python
# Full image: ~1GB, Slim image: ~150MB
FROM python:3.11-slim

# ==============================================================================
# WORKING DIRECTORY
# ==============================================================================
# Set the working directory inside the container
# All subsequent commands will run from this directory
# COPY and ADD commands will use this as the destination base
WORKDIR /app

# ==============================================================================
# ENVIRONMENT VARIABLES
# ==============================================================================
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
# This keeps the container cleaner and reduces image size
ENV PYTHONDONTWRITEBYTECODE=1

# PYTHONUNBUFFERED: Forces Python output to be unbuffered
# Ensures logs appear immediately in container logs (docker logs)
# Important for debugging and monitoring
ENV PYTHONUNBUFFERED=1

# FLASK_APP: Tells Flask which file contains the application
ENV FLASK_APP=app.py

# FLASK_ENV: Sets the Flask environment
# 'production' disables debug mode and enables optimizations
ENV FLASK_ENV=production

# ==============================================================================
# DEPENDENCY INSTALLATION
# ==============================================================================
# Copy requirements.txt first (before other files)
# This leverages Docker's layer caching:
#   - Dependencies only reinstall when requirements.txt changes
#   - Speeds up builds when only application code changes
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir: Don't store pip cache, reduces image size
RUN pip install --no-cache-dir -r requirements.txt

# ==============================================================================
# APPLICATION CODE
# ==============================================================================
# Copy all application files to the container
# This is done after pip install to leverage layer caching
COPY . .

# ==============================================================================
# SECURITY: NON-ROOT USER
# ==============================================================================
# Create a non-root user for running the application
# Security best practice: containers should not run as root
# --disabled-password: No password login (container only)
# --gecos '': Skip interactive user info prompts
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user for all subsequent commands
# The application will run with limited privileges
USER appuser

# ==============================================================================
# PORT CONFIGURATION
# ==============================================================================
# Expose port 5000 for the Flask application
# This is documentation - actual port mapping is done at runtime
# docker run -p 5000:5000 or in docker-compose.yml
EXPOSE 5000

# ==============================================================================
# HEALTH CHECK
# ==============================================================================
# Configure container health monitoring
# Docker and orchestrators use this to determine container health
#
# Parameters:
#   --interval=30s: Check every 30 seconds
#   --timeout=10s: Wait up to 10 seconds for response
#   --start-period=5s: Grace period for container startup
#   --retries=3: Mark unhealthy after 3 consecutive failures
#
# The health check calls our /health endpoint
# Returns 0 (healthy) if HTTP 200, 1 (unhealthy) otherwise
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# ==============================================================================
# APPLICATION STARTUP COMMAND
# ==============================================================================
# Run the application using Gunicorn WSGI server
# Gunicorn is production-ready, unlike Flask's development server
#
# Parameters:
#   --bind 0.0.0.0:5000: Listen on all interfaces, port 5000
#   --workers 2: Number of worker processes (typically 2*CPU+1)
#   app:app: Module:application (app.py contains 'app' Flask instance)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
