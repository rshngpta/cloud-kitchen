pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'cloud-kitchen'
        DOCKER_TAG = "${BUILD_NUMBER}"
        APP_NAME = 'cloud-kitchen'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Security Scan - Dependencies') {
            steps {
                echo 'Scanning dependencies for vulnerabilities...'
                sh '''
                    . venv/bin/activate
                    pip install safety
                    safety check -r requirements.txt --continue-on-error || true
                '''
            }
        }
        
        stage('Lint') {
            steps {
                echo 'Running linting checks...'
                sh '''
                    . venv/bin/activate
                    pip install flake8
                    flake8 app.py models.py forms.py config.py --max-line-length=120 --ignore=E501 || true
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    . venv/bin/activate
                    pip install pytest pytest-flask pytest-cov
                    python -m pytest tests/ -v --cov=. --cov-report=xml --cov-report=html || true
                '''
            }
            post {
                always {
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                '''
            }
        }
        
        stage('Security Scan - Docker Image') {
            steps {
                echo 'Scanning Docker image for vulnerabilities...'
                sh '''
                    # Using Trivy for container scanning (install if needed)
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy:latest image --severity HIGH,CRITICAL \
                        ${DOCKER_IMAGE}:${DOCKER_TAG} || true
                '''
            }
        }
        
        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                echo 'Pushing Docker image to registry...'
                withCredentials([usernamePassword(credentialsId: 'docker-registry', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                echo 'Deploying to staging environment...'
                sh '''
                    docker-compose down || true
                    docker-compose up -d
                '''
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying to production environment...'
                sh '''
                    # Stop existing container
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true
                    
                    # Run new container
                    docker run -d \
                        --name ${APP_NAME} \
                        -p 5000:5000 \
                        --restart unless-stopped \
                        -e SECRET_KEY=${SECRET_KEY} \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }
        
        stage('Health Check') {
            steps {
                echo 'Performing health check...'
                sh '''
                    sleep 10
                    curl -f http://localhost:5000/health || exit 1
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh 'docker system prune -f || true'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}

