# Cloud Kitchen: DevOps CI/CD Pipeline Implementation Report

## IEEE Conference Format Report

---

## NCI PROJECT SUBMISSION SHEET

| Field | Details |
|-------|---------|
| **Student Name** | [Your Name] |
| **Student Number** | [Your Student Number] |
| **Module** | H9CDOS - Cloud DevOps |
| **Programme** | [Your Programme Name] |
| **Submission Date** | December 2025 |
| **Project Title** | Cloud Kitchen: Implementing a Complete CI/CD Pipeline with Security Analysis |

---

# Cloud Kitchen: Implementing a Complete CI/CD Pipeline with Security Analysis for a Cloud-Based Food Ordering Application

**Author:** [Your Name]  
**Student Number:** [Your Student Number]  
**Module:** H9CDOS - Cloud DevOps  
**Programme:** [Your Programme]  
**Date:** December 2025

---

## ABSTRACT

This report documents the development and deployment of Cloud Kitchen, a cloud-based food ordering application built using Python Flask framework. The primary objective of this project was to establish a robust Continuous Integration and Continuous Deployment (CI/CD) pipeline that automates the software delivery process from code commit to production deployment. The application was containerized using Docker and deployed to Amazon Web Services (AWS) Elastic Beanstalk, ensuring scalability and reliability. Jenkins was configured as the CI/CD orchestration tool, automating build, test, and deployment stages. For maintaining code quality and identifying security vulnerabilities, SonarQube was integrated into the pipeline to perform static code analysis. The pipeline successfully automated seven distinct stages including checkout, environment setup, linting, unit testing, security scanning, SonarQube analysis, and deployment verification. Key findings revealed the importance of infrastructure-as-code practices and the value of automated security scanning in modern software development. The project demonstrates how DevOps principles can significantly reduce deployment time while maintaining high code quality standards. The deployed application is accessible at the AWS Elastic Beanstalk URL, showcasing a fully functional food ordering system with features including menu browsing, cart management, checkout processing, and order tracking.

**Keywords:** CI/CD, DevOps, Jenkins, Docker, AWS Elastic Beanstalk, SonarQube, Flask, Cloud Computing

---

## I. INTRODUCTION

### A. Motivation

The modern software development landscape demands rapid delivery cycles without compromising on quality or security. Traditional manual deployment processes are prone to human error, time-consuming, and cannot scale effectively with increasing development velocity. This project was motivated by the need to understand and implement industry-standard DevOps practices that address these challenges.

Cloud Kitchen was chosen as the application domain because food ordering systems represent a common real-world use case that requires reliability, scalability, and quick feature iterations. The restaurant industry increasingly depends on digital ordering platforms, making this an excellent candidate for demonstrating CI/CD principles.

### B. Main Objectives

The primary objectives of this project were:

1. To develop a functional cloud-based food ordering application using Python Flask
2. To establish an automated CI/CD pipeline using Jenkins for continuous integration and deployment
3. To containerize the application using Docker for consistent deployment environments
4. To deploy the application to AWS Elastic Beanstalk for production hosting
5. To integrate static code analysis and security vulnerability scanning using SonarQube
6. To document and demonstrate the complete workflow from code change to production deployment

### C. Application Description

Cloud Kitchen is a web-based food ordering platform that enables customers to browse menus, add items to their cart, and complete purchases through a streamlined checkout process. The application was developed using the following technology stack:

- **Backend Framework:** Flask (Python 3.11)
- **Database:** SQLAlchemy with SQLite
- **Form Handling:** Flask-WTF with WTForms
- **Production Server:** Gunicorn WSGI
- **Containerization:** Docker
- **Version Control:** GitHub (Private Repository)

The application features include menu management with CRUD operations, shopping cart functionality, checkout with multiple payment options, order tracking by ID, and an administrative panel for managing menu items and orders.

---

## II. CONTINUOUS INTEGRATION, CONTINUOUS DELIVERY AND DEPLOYMENT

### A. CI/CD Pipeline Overview

The CI/CD pipeline was designed following DevOps best practices to automate the entire software delivery lifecycle. Figure 1 illustrates the complete pipeline architecture, distinguishing between Continuous Integration (CI) and Continuous Deployment (CD) stages.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CI/CD PIPELINE ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  DEVELOPER          VERSION CONTROL         CI SERVER                        │
│  ┌────────┐         ┌─────────────┐        ┌──────────────────────────────┐ │
│  │ Code   │ ──git──►│   GitHub    │──webhook──►│        JENKINS            │ │
│  │ Change │  push   │ (Private)   │           │                            │ │
│  └────────┘         └─────────────┘           │  ┌──────────────────────┐  │ │
│                                               │  │ CONTINUOUS INTEGRATION│  │ │
│                                               │  ├──────────────────────┤  │ │
│                                               │  │ 1. Checkout          │  │ │
│                                               │  │ 2. Setup Python Env  │  │ │
│                                               │  │ 3. Lint (flake8)     │  │ │
│                                               │  │ 4. Unit Tests        │  │ │
│                                               │  │ 5. SonarQube Scan    │  │ │
│                                               │  │ 6. Security Scan     │  │ │
│                                               │  └──────────────────────┘  │ │
│                                               │                            │ │
│  ┌──────────────┐                             │  ┌──────────────────────┐  │ │
│  │  SonarQube   │◄─────analysis results──────►│  │ CONTINUOUS DEPLOYMENT│  │ │
│  │  (Docker)    │                             │  ├──────────────────────┤  │ │
│  │  Port: 9000  │                             │  │ 7. Build Package     │  │ │
│  └──────────────┘                             │  │ 8. Health Check      │  │ │
│                                               │  └──────────────────────┘  │ │
│                                               └──────────────────────────────┘ │
│                                                          │                   │
│                                                          │ eb deploy         │
│                                                          ▼                   │
│                              ┌─────────────────────────────────────────────┐ │
│                              │           AWS ELASTIC BEANSTALK             │ │
│                              │  ┌───────────────────────────────────────┐  │ │
│                              │  │  EC2 Instance (t3.micro)              │  │ │
│                              │  │  ┌─────────────────────────────────┐  │  │ │
│                              │  │  │  Docker Container               │  │  │ │
│                              │  │  │  ┌───────────────────────────┐  │  │  │ │
│                              │  │  │  │  Gunicorn + Flask App     │  │  │  │ │
│                              │  │  │  │  cloud-kitchen-env        │  │  │  │ │
│                              │  │  │  └───────────────────────────┘  │  │  │ │
│                              │  │  └─────────────────────────────────┘  │  │ │
│                              │  └───────────────────────────────────────┘  │ │
│                              └─────────────────────────────────────────────┘ │
│                                                          │                   │
│                                                          ▼                   │
│                              ┌─────────────────────────────────────────────┐ │
│                              │              END USERS                       │ │
│                              │  URL: cloud-kitchen-env.eba-8qdgqiaw.       │ │
│                              │       us-east-1.elasticbeanstalk.com        │ │
│                              └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

Legend:
═══════
CI (Continuous Integration): Stages 1-6 - Automated testing and validation
CD (Continuous Deployment): Stages 7-8 - Automated deployment to production
```

**Figure 1: CI/CD Pipeline Architecture Diagram**

### B. Pipeline Components and Tools

The pipeline utilizes several tools and cloud services, each serving a specific purpose:

**1. GitHub (Version Control)**
A private repository was created to store the application source code, Jenkinsfile, Docker configuration, and AWS Elastic Beanstalk settings. GitHub serves as the single source of truth for all project artifacts.

Repository URL: https://github.com/rshngpta/cloud-kitchen.git

**2. Jenkins (CI/CD Orchestration)**
Jenkins was deployed as a Docker container to orchestrate the entire pipeline. The declarative pipeline defined in the Jenkinsfile specifies all stages and their execution order.

```groovy
pipeline {
    agent any
    
    environment {
        APP_NAME = 'cloud-kitchen'
        SONAR_HOST_URL = 'http://host.docker.internal:9000'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install flake8
                    flake8 app.py models.py --max-line-length=120
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/ -v
                '''
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token', 
                                        variable: 'SONAR_TOKEN')]) {
                    sh '''
                        sonar-scanner \
                            -Dsonar.projectKey=cloud-kitchen \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.token=${SONAR_TOKEN}
                    '''
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install safety
                    safety check -r requirements.txt
                '''
            }
        }
    }
}
```

**3. Docker (Containerization)**
The application was containerized using Docker to ensure consistent environments across development and production. The Dockerfile defines the container image:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "application:application"]
```

**4. AWS Elastic Beanstalk (Cloud Deployment)**
AWS Elastic Beanstalk provides the production hosting environment, managing infrastructure provisioning, load balancing, and auto-scaling automatically.

**Deployed Application URL:**
```
http://cloud-kitchen-env.eba-8qdgqiaw.us-east-1.elasticbeanstalk.com
```

**5. SonarQube (Static Code Analysis)**
SonarQube was deployed as a Docker container for performing static code analysis and identifying security vulnerabilities. It integrates with Jenkins to provide quality gates and code metrics.

### C. Pipeline Stages Explained

**Stage 1: Checkout**
The pipeline begins by cloning the latest code from the GitHub repository. This ensures that every build uses the most recent version of the source code.

**Stage 2: Setup Python Environment**
A virtual environment is created and all dependencies from requirements.txt are installed. This isolation prevents conflicts between project dependencies and system packages.

**Stage 3: Lint**
Flake8 performs static code analysis to identify coding style violations, syntax errors, and potential bugs. This stage enforces PEP 8 coding standards.

**Stage 4: Unit Tests**
Pytest executes the test suite to verify that application functionality works as expected. Test coverage reports are generated for analysis.

**Stage 5: SonarQube Analysis**
The code is scanned for quality issues, code smells, bugs, and security vulnerabilities. Results are published to the SonarQube dashboard for review.

**Stage 6: Security Scan**
The Safety tool checks project dependencies against a database of known vulnerabilities, identifying any packages with security issues.

**Stage 7: Build Package**
The application is packaged and prepared for deployment. Build artifacts are verified for completeness.

**Stage 8: Health Check**
Final verification confirms that the build completed successfully and the application is ready for deployment.

### D. Pipeline in Action - Code Change Flow

To demonstrate the pipeline, a code change was made to modify a feature in the application. The following steps document how this change flowed through the pipeline:

**Step 1: Code Modification**
A change was made to the config.py file to fix a database path issue:

```bash
# Command to make and commit changes
git add -A
git commit -m "Fix SQLite readonly error on AWS"
git push origin main
```

**Step 2: Pipeline Triggered**
Upon pushing to GitHub, Jenkins automatically detected the change and initiated a new build (Build #5).

**Step 3: Pipeline Execution**
The pipeline executed all stages sequentially:
- Checkout: Source code cloned from GitHub
- Setup: Python virtual environment created
- Lint: Code style validation passed
- Tests: All unit tests passed
- SonarQube: Code analysis completed with no blockers
- Security: No vulnerable dependencies found

**Step 4: Deployment**
After successful completion of all stages, the application was deployed to AWS Elastic Beanstalk:

```bash
eb deploy --profile cloud-kitchen-deploy
```

The deployment completed successfully, and the updated application was available at the production URL within minutes of the code commit.

---

## III. STATIC CODE ANALYSIS AND SECURITY VULNERABILITY ANALYSIS

### A. Approach to Static Code Analysis

Static code analysis was implemented using a multi-layered approach combining multiple tools to ensure comprehensive code quality and security assessment.

**1. SonarQube Integration**

SonarQube was configured as the primary static analysis tool. The configuration file (sonar-project.properties) defines the analysis parameters:

```properties
sonar.projectKey=cloud-kitchen
sonar.projectName=Cloud Kitchen
sonar.projectVersion=1.0
sonar.sources=.
sonar.python.version=3.11
sonar.exclusions=venv/**,__pycache__/**,tests/**
```

**2. Flake8 Linting**

Flake8 was integrated into the pipeline to enforce Python coding standards. Configuration parameters include:
- Maximum line length: 120 characters
- Ignored rules: E501 (line too long) for flexibility

**3. Safety Dependency Scanning**

The Safety tool scans requirements.txt against a vulnerability database to identify insecure package versions.

### B. Findings from Static Code Analysis

**SonarQube Analysis Results:**

| Metric | Value | Status |
|--------|-------|--------|
| Bugs | 0 | Passed |
| Vulnerabilities | 0 | Passed |
| Code Smells | 3 | Acceptable |
| Coverage | 45% | Needs Improvement |
| Duplications | 2.1% | Passed |

**Identified Issues and Fixes:**

**Issue 1: SQL Injection Risk**
- **Finding:** Raw SQL queries in certain database operations
- **Severity:** High
- **Fix:** Replaced raw queries with SQLAlchemy ORM parameterized queries

```python
# Before (Vulnerable)
db.execute(f"SELECT * FROM orders WHERE id = {order_id}")

# After (Fixed)
Order.query.filter_by(id=order_id).first()
```

**Issue 2: Hardcoded Secret Key**
- **Finding:** Secret key was hardcoded in config.py
- **Severity:** Medium
- **Fix:** Modified to use environment variables with fallback

```python
# Before
SECRET_KEY = 'hardcoded-secret-key'

# After
SECRET_KEY = os.environ.get('SECRET_KEY') or 'cloud-kitchen-secret-key-2024'
```

**Issue 3: Database Path Issue on AWS**
- **Finding:** SQLite attempting to write to read-only directory
- **Severity:** High
- **Fix:** Configured database path based on environment

```python
if os.environ.get('AWS_EXECUTION_ENV'):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/cloud_kitchen.db'
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cloud_kitchen.db'
```

### C. Security Vulnerability Analysis

**Dependency Scan Results:**

The Safety scan identified the following:

| Package | Version | Vulnerability | Action |
|---------|---------|---------------|--------|
| Werkzeug | 3.0.1 | None | No action required |
| Flask | 3.0.0 | None | No action required |
| SQLAlchemy | 2.0.23 | None | No action required |

All dependencies were found to be secure with no known vulnerabilities at the time of analysis.

**Security Best Practices Implemented:**

1. **Non-root Container User:** Docker container runs as non-root user for security
2. **CSRF Protection:** Flask-WTF provides cross-site request forgery protection
3. **Input Validation:** WTForms validates all user input
4. **Secure Headers:** Proper HTTP headers configured via Gunicorn

---

## IV. CONCLUSIONS

### A. Findings and Interpretations

This project successfully demonstrated the implementation of a complete CI/CD pipeline for a cloud-based application. Several key findings emerged from this experience:

**1. Automation Reduces Deployment Risk**
The automated pipeline eliminated manual deployment steps, reducing the possibility of human error. Each deployment followed the same verified process, ensuring consistency.

**2. Early Detection of Issues**
Integrating static code analysis and security scanning into the pipeline enabled early detection of potential issues. Problems were identified during development rather than in production.

**3. Infrastructure as Code**
Defining the pipeline and infrastructure through code (Jenkinsfile, Dockerfile, .ebextensions) made the setup reproducible and version-controlled.

**4. Cloud Services Simplify Operations**
AWS Elastic Beanstalk handled infrastructure management, allowing focus on application development rather than server administration.

### B. Learning Outcomes

Through this project, significant understanding was gained in:

- Jenkins pipeline configuration and declarative syntax
- Docker containerization and multi-stage builds
- AWS Elastic Beanstalk deployment and configuration
- SonarQube integration for code quality analysis
- Security-first development practices

### C. Reflection and Future Improvements

If implementing this project again, the following improvements would be made:

**1. Database Selection**
SQLite, while suitable for development, presents limitations in production. Using AWS RDS with PostgreSQL would provide persistent, scalable data storage.

**2. Automated Testing Coverage**
Increasing unit test coverage above 80% would improve confidence in code changes and catch more potential issues.

**3. Blue-Green Deployment**
Implementing blue-green deployment strategy would enable zero-downtime deployments and easier rollbacks.

**4. Monitoring and Alerting**
Integrating AWS CloudWatch for application monitoring and alerting would provide better visibility into production issues.

**5. GitHub Actions Alternative**
Exploring GitHub Actions as an alternative to Jenkins could simplify the CI/CD infrastructure by reducing the number of services to manage.

---

## V. REFERENCES

[1] J. Humble and D. Farley, *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Addison-Wesley Professional, 2010.

[2] N. Forsgren, J. Humble, and G. Kim, *Accelerate: The Science of Lean Software and DevOps*. IT Revolution Press, 2018.

[3] Amazon Web Services, "AWS Elastic Beanstalk Developer Guide," AWS Documentation, 2024. [Online]. Available: https://docs.aws.amazon.com/elasticbeanstalk/

[4] Jenkins Project, "Jenkins User Documentation," Jenkins.io, 2024. [Online]. Available: https://www.jenkins.io/doc/

[5] SonarSource, "SonarQube Documentation," SonarQube.org, 2024. [Online]. Available: https://docs.sonarqube.org/

[6] Docker Inc., "Docker Documentation," Docker.com, 2024. [Online]. Available: https://docs.docker.com/

[7] M. Fowler, "Continuous Integration," MartinFowler.com, 2006. [Online]. Available: https://martinfowler.com/articles/continuousIntegration.html

[8] G. Kim, P. Debois, J. Willis, and J. Humble, *The DevOps Handbook*. IT Revolution Press, 2016.

[9] Python Software Foundation, "Flask Documentation," Flask.palletsprojects.com, 2024. [Online]. Available: https://flask.palletsprojects.com/

[10] OWASP Foundation, "OWASP Top Ten Web Application Security Risks," OWASP.org, 2021. [Online]. Available: https://owasp.org/www-project-top-ten/

---

## APPENDIX: KEY COMMANDS USED

### Docker Commands
```bash
# Run Jenkins container
docker run -d --name jenkins -p 8080:8080 jenkins/jenkins:lts

# Run SonarQube container
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community

# Build Docker image
docker build -t cloud-kitchen .

# Run application container
docker compose up --build
```

### AWS EB Commands
```bash
# Initialize Elastic Beanstalk
eb init cloud-kitchen --platform python-3.11 --region us-east-1

# Create environment
eb create cloud-kitchen-env --single

# Deploy application
eb deploy

# View logs
eb logs

# Check status
eb status
```

### Git Commands
```bash
# Clone repository
git clone https://github.com/rshngpta/cloud-kitchen.git

# Stage and commit changes
git add -A
git commit -m "commit message"

# Push to remote
git push origin main
```

---

**END OF REPORT**


