# Cloud Kitchen - DevOps Project

A dynamic cloud-based food ordering application with full CI/CD pipeline integration.

## Features

- **Menu Management (CRUD)**: Add, view, edit, and delete menu items
- **Cart Functionality**: Add items, update quantities, remove items
- **Order Placement**: Complete checkout with customer details
- **Payment Handling**: Support for card and cash on delivery
- **Order Tracking**: Track orders by order ID
- **Admin Panel**: Manage menu items and orders

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (can be configured for PostgreSQL/MySQL)
- **Frontend**: HTML, CSS (basic)
- **Containerization**: Docker
- **CI/CD**: Jenkins
- **Security**: CSRF protection, input validation

## Project Structure

```
Cloud_Kitchen/
├── app.py              # Main Flask application
├── models.py           # Database models
├── forms.py            # WTForms for validation
├── config.py           # Application configuration
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── Jenkinsfile         # CI/CD pipeline
├── templates/          # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── menu.html
│   ├── cart.html
│   ├── checkout.html
│   ├── payment.html
│   ├── orders.html
│   └── ...
└── tests/              # Unit tests
    ├── conftest.py
    └── test_app.py
```

## Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Cloud_Kitchen
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open http://localhost:5000 in your browser

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually**
   ```bash
   docker build -t cloud-kitchen .
   docker run -p 5000:5000 cloud-kitchen
   ```

## CI/CD Pipeline (Jenkins)

The Jenkinsfile includes the following stages:

1. **Checkout**: Clone source code
2. **Setup**: Create Python virtual environment
3. **Security Scan**: Check dependencies for vulnerabilities
4. **Lint**: Code quality checks with flake8
5. **Unit Tests**: Run pytest with coverage
6. **Build**: Create Docker image
7. **Security Scan**: Scan Docker image with Trivy
8. **Deploy**: Deploy to staging/production

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/menu` | GET | Browse menu |
| `/cart` | GET | View cart |
| `/checkout` | GET, POST | Checkout process |
| `/payment` | GET, POST | Payment processing |
| `/orders` | GET | View all orders |
| `/track` | GET, POST | Track order |
| `/health` | GET | Health check |
| `/api/menu` | GET | API: Get menu items |
| `/api/order/<id>` | GET | API: Get order details |

## Security Features

- CSRF Protection (Flask-WTF)
- Input Validation (WTForms validators)
- SQL Injection Prevention (SQLAlchemy ORM)
- Non-root Docker user
- Environment variable configuration

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=. --cov-report=html
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| SECRET_KEY | Flask secret key | cloud-kitchen-secret-key-2024 |
| DATABASE_URL | Database connection URL | sqlite:///cloud_kitchen.db |
| DEBUG | Debug mode | False |
| PORT | Application port | 5000 |

## Cloud Deployment

This application can be deployed to:
- AWS (EC2, ECS, Elastic Beanstalk)
- Azure (App Service, Container Instances)
- Google Cloud (App Engine, Cloud Run)
- Heroku
- DigitalOcean (App Platform, Droplets)
- Render

## License

This project is created for educational purposes as part of the Cloud DevOpsSec module.

## Author

Raushan kumar - 2025

