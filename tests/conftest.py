import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import MenuItem, Order, OrderItem


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Add sample menu item
            item = MenuItem(
                name='Test Item',
                description='Test description',
                price=9.99,
                category='main_course',
                available=True
            )
            db.session.add(item)
            db.session.commit()
        yield client


@pytest.fixture
def sample_menu_item():
    """Sample menu item data"""
    return {
        'name': 'Pizza',
        'description': 'Delicious pizza',
        'price': 12.99,
        'category': 'main_course',
        'available': True
    }


@pytest.fixture
def sample_order_data():
    """Sample order data"""
    return {
        'customer_name': 'John Doe',
        'customer_email': 'john@example.com',
        'customer_phone': '+1234567890',
        'customer_address': '123 Test Street, Test City, TC 12345'
    }

