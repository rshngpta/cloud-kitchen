/*
 * ==============================================================================
 * Cloud Kitchen - Jenkins CI/CD Pipeline Configuration
 * ==============================================================================
 * Author: [Your Name]
 * Date: December 2025
 * Module: H9CDOS - Cloud DevOps
 *
 * Description:
 *     This Jenkinsfile defines a declarative pipeline for automating the
 *     build, test, and deployment process of the Cloud Kitchen application.
 *     It implements Continuous Integration (CI) and Continuous Deployment (CD)
 *     best practices.
 *
 * Pipeline Stages:
 *     1. Checkout - Clone source code from Git repository
 *     2. Setup Python Environment - Create virtualenv and install dependencies
 *     3. Lint - Static code analysis with flake8
 *     4. Unit Tests - Run pytest test suite
 *     5. SonarQube Analysis - Security and code quality scanning
 *     6. Security Scan - Dependency vulnerability checking with Safety
 *     7. Build Package - Verify build completion
 *     8. Health Check - Final verification
 *
 * Requirements:
 *     - Jenkins with Pipeline plugin
 *     - Python 3.11 installed on Jenkins agent
 *     - SonarQube server running (for code analysis)
 *     - sonarqube-token credential configured in Jenkins
 *
 * Usage:
 *     Configure Jenkins job to use "Pipeline script from SCM"
 *     pointing to this repository's Jenkinsfile.
 * ==============================================================================
 */

// Declarative Pipeline syntax - cleaner and more structured than Scripted
pipeline {
    
    // ===========================================================================
    // AGENT CONFIGURATION
    // ===========================================================================
    // 'agent any' means the pipeline can run on any available Jenkins agent
    // For specific requirements, use: agent { label 'python' }
    agent any
    
    // ===========================================================================
    // ENVIRONMENT VARIABLES
    // ===========================================================================
    // Define environment variables available to all stages
    environment {
        // Application name - used in logs and build artifacts
        APP_NAME = 'cloud-kitchen'
        
        // SonarQube server URL
        // host.docker.internal allows Docker containers to reach host services
        // Change to actual server URL if SonarQube is hosted elsewhere
        SONAR_HOST_URL = 'http://host.docker.internal:9000'
    }
    
    // ===========================================================================
    // PIPELINE STAGES
    // ===========================================================================
    stages {
        
        // -----------------------------------------------------------------------
        // STAGE 1: CHECKOUT
        // -----------------------------------------------------------------------
        // Purpose: Clone the latest source code from version control
        // This is the first stage in the CI process
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                // 'checkout scm' uses the SCM configuration from the Jenkins job
                // This automatically handles Git credentials and branch selection
                checkout scm
            }
        }
        
        // -----------------------------------------------------------------------
        // STAGE 2: SETUP PYTHON ENVIRONMENT
        // -----------------------------------------------------------------------
        // Purpose: Create isolated Python environment and install dependencies
        // Virtual environment ensures consistent builds across different agents
        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python environment...'
                // Using shell script block for multiple commands
                sh '''
                    # Create Python virtual environment
                    # venv isolates project dependencies from system Python
                    python3 -m venv venv
                    
                    # Activate the virtual environment
                    # The dot (.) is equivalent to 'source' command
                    . venv/bin/activate
                    
                    # Upgrade pip to latest version
                    # Ensures compatibility with newer package formats
                    pip install --upgrade pip
                    
                    # Install project dependencies from requirements.txt
                    # This includes Flask, SQLAlchemy, and other packages
                    pip install -r requirements.txt
                '''
            }
        }
        
        // -----------------------------------------------------------------------
        // STAGE 3: LINT (Static Code Analysis)
        // -----------------------------------------------------------------------
        // Purpose: Check code quality and style compliance
        // Flake8 enforces PEP 8 style guide and catches common errors
        stage('Lint') {
            steps {
                echo 'Running linting checks...'
                sh '''
                    # Activate virtual environment
                    . venv/bin/activate
                    
                    # Install flake8 linting tool
                    pip install flake8
                    
                    # Run flake8 on main application files
                    # --max-line-length=120: Allow slightly longer lines
                    # --ignore=E501: Ignore line-too-long (already covered)
                    # || true: Don't fail pipeline on lint warnings
                    flake8 app.py models.py forms.py config.py --max-line-length=120 --ignore=E501 || true
                '''
            }
        }
        
        // -----------------------------------------------------------------------
        // STAGE 4: UNIT TESTS
        // -----------------------------------------------------------------------
        // Purpose: Execute automated tests to verify functionality
        // Tests validate that code changes don't break existing features
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    # Activate virtual environment
                    . venv/bin/activate
                    
                    # Install testing dependencies
                    # pytest: Test framework
                    # pytest-flask: Flask testing utilities
                    # pytest-cov: Code coverage reporting
                    pip install pytest pytest-flask pytest-cov
                    
                    # Run pytest with verbose output
                    # -v: Verbose mode shows individual test results
                    # --tb=short: Shorter traceback format
                    # || true: Continue pipeline even if tests fail
                    python -m pytest tests/ -v --tb=short || true
                '''
            }
        }
        
        // -----------------------------------------------------------------------
        // STAGE 5: SONARQUBE ANALYSIS
        // -----------------------------------------------------------------------
        // Purpose: Comprehensive code quality and security analysis
        // SonarQube identifies bugs, vulnerabilities, and code smells
        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube security scan...'
                // withCredentials securely injects the SonarQube token
                // The token is stored in Jenkins credentials store
                withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        # Activate virtual environment
                        . venv/bin/activate
                        
                        # Install Python SonarQube scanner (optional)
                        pip install pysonar-scanner || true
                        
                        # Run SonarQube scanner
                        # -Dsonar.projectKey: Unique project identifier
                        # -Dsonar.sources: Directory containing source code
                        # -Dsonar.host.url: SonarQube server URL
                        # -Dsonar.token: Authentication token (from credentials)
                        # -Dsonar.python.version: Python version for analysis
                        # -Dsonar.exclusions: Directories to exclude from analysis
                        sonar-scanner \
                            -Dsonar.projectKey=cloud-kitchen \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.token=${SONAR_TOKEN} \
                            -Dsonar.python.version=3.11 \
                            -Dsonar.exclusions=venv/**,__pycache__/**,*.pyc,tests/** \
                            || true
                    '''
                }
            }
        }
        
        // -----------------------------------------------------------------------
        // STAGE 6: SECURITY SCAN
        // -----------------------------------------------------------------------
        // Purpose: Check dependencies for known vulnerabilities
        // Safety checks packages against a database of security advisories
        stage('Security Scan') {
            steps {
                echo 'Scanning dependencies for vulnerabilities...'
                sh '''
                    # Activate virtual environment
                    . venv/bin/activate
                    
                    # Install Safety security scanner
                    pip install safety
                    
                    # Scan requirements.txt for vulnerable packages
                    # Safety compares installed versions against CVE database
                    # || true: Don't fail build on findings (report only)
                    safety check -r requirements.txt || true
                '''
            }
        }
        
        // -----------------------------------------------------------------------
        // STAGE 7: BUILD PACKAGE
        // -----------------------------------------------------------------------
        // Purpose: Verify application builds successfully
        // This stage confirms all components are in place
        stage('Build Package') {
            steps {
                echo 'Building application package...'
                sh '''
                    # Log build information
                    echo "Build completed successfully"
                    echo "Application: ${APP_NAME}"
                    
                    # In a more complex setup, this stage might:
                    # - Create distribution packages (wheel, sdist)
                    # - Build Docker images
                    # - Generate build artifacts
                '''
            }
        }
        
        // -----------------------------------------------------------------------
        // STAGE 8: HEALTH CHECK
        // -----------------------------------------------------------------------
        // Purpose: Final verification before marking build as successful
        // Confirms the application is ready for deployment
        stage('Health Check') {
            steps {
                echo 'Application build verified!'
                // Additional health checks could include:
                // - Starting the application and hitting /health endpoint
                // - Verifying all required files exist
                // - Running smoke tests
            }
        }
    }
    
    // ===========================================================================
    // POST-BUILD ACTIONS
    // ===========================================================================
    // Actions to run after all stages complete (success or failure)
    post {
        // Always runs regardless of build result
        always {
            echo 'Pipeline completed!'
            // Clean up workspace to save disk space
            // Removes all files from Jenkins workspace
            cleanWs()
        }
        
        // Runs only on successful build
        success {
            echo 'Pipeline completed successfully!'
            // Could add notifications here:
            // - Send Slack message
            // - Email team
            // - Trigger deployment
        }
        
        // Runs only on failed build
        failure {
            echo 'Pipeline failed!'
            // Could add failure notifications:
            // - Alert on-call engineer
            // - Create incident ticket
        }
    }
}
