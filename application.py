# Elastic Beanstalk looks for 'application' as the callable by default
# This file imports the Flask app and exposes it as 'application'

from app import app as application

# For local development
if __name__ == '__main__':
    application.run(debug=True)


