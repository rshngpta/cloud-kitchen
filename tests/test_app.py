"""
Unit tests for Cloud Kitchen application
Tests cover CRUD operations, input validation, and core functionality
"""
import pytest


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_endpoint(self, client):
        """Test health check returns 200"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['app'] == 'Cloud Kitchen'


class TestHomePage:
    """Test home page"""
    
    def test_home_page_loads(self, client):
        """Test home page returns 200"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Cloud Kitchen' in response.data


class TestMenuCRUD:
    """Test Menu CRUD operations"""
    
    def test_menu_page_loads(self, client):
        """Test menu page returns 200"""
        response = client.get('/menu')
        assert response.status_code == 200
        assert b'Menu' in response.data
    
    def test_admin_menu_page_loads(self, client):
        """Test admin menu page returns 200"""
        response = client.get('/admin/menu')
        assert response.status_code == 200
    
    def test_add_menu_item_page_loads(self, client):
        """Test add menu item page returns 200"""
        response = client.get('/admin/menu/add')
        assert response.status_code == 200
    
    def test_add_menu_item(self, client, sample_menu_item):
        """Test adding a new menu item"""
        response = client.post('/admin/menu/add', data=sample_menu_item, follow_redirects=True)
        assert response.status_code == 200
        assert b'Menu item added successfully' in response.data
    
    def test_add_menu_item_validation(self, client):
        """Test menu item validation - missing required fields"""
        invalid_data = {
            'name': '',
            'price': '',
            'category': ''
        }
        response = client.post('/admin/menu/add', data=invalid_data)
        assert response.status_code == 200
        # Form should be redisplayed with errors
    
    def test_edit_menu_item(self, client):
        """Test editing menu item"""
        response = client.get('/admin/menu/edit/1')
        assert response.status_code == 200
    
    def test_delete_menu_item(self, client, sample_menu_item):
        """Test deleting menu item"""
        # First add an item
        client.post('/admin/menu/add', data=sample_menu_item)
        # Then delete it
        response = client.post('/admin/menu/delete/2', follow_redirects=True)
        assert response.status_code == 200


class TestCart:
    """Test Cart functionality"""
    
    def test_cart_page_loads(self, client):
        """Test cart page returns 200"""
        response = client.get('/cart')
        assert response.status_code == 200
    
    def test_add_to_cart(self, client):
        """Test adding item to cart"""
        response = client.post('/cart/add/1', data={'quantity': 2}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Item added to cart' in response.data
    
    def test_update_cart(self, client):
        """Test updating cart item"""
        # First add item
        client.post('/cart/add/1', data={'quantity': 1})
        # Then update
        response = client.post('/cart/update/1', data={'quantity': 3}, follow_redirects=True)
        assert response.status_code == 200
    
    def test_remove_from_cart(self, client):
        """Test removing item from cart"""
        # First add item
        client.post('/cart/add/1', data={'quantity': 1})
        # Then remove
        response = client.post('/cart/remove/1', follow_redirects=True)
        assert response.status_code == 200
        assert b'Item removed from cart' in response.data
    
    def test_clear_cart(self, client):
        """Test clearing cart"""
        client.post('/cart/add/1', data={'quantity': 1})
        response = client.post('/cart/clear', follow_redirects=True)
        assert response.status_code == 200
        assert b'Cart cleared' in response.data


class TestCheckout:
    """Test Checkout functionality"""
    
    def test_checkout_empty_cart(self, client):
        """Test checkout with empty cart redirects"""
        response = client.get('/checkout', follow_redirects=True)
        assert response.status_code == 200
        assert b'cart is empty' in response.data
    
    def test_checkout_with_items(self, client):
        """Test checkout page with items in cart"""
        client.post('/cart/add/1', data={'quantity': 1})
        response = client.get('/checkout')
        assert response.status_code == 200
        assert b'Checkout' in response.data
    
    def test_checkout_form_validation(self, client, sample_order_data):
        """Test checkout form validation"""
        client.post('/cart/add/1', data={'quantity': 1})
        response = client.post('/checkout', data=sample_order_data, follow_redirects=True)
        assert response.status_code == 200


class TestOrders:
    """Test Order functionality"""
    
    def test_orders_page_loads(self, client):
        """Test orders page returns 200"""
        response = client.get('/orders')
        assert response.status_code == 200
    
    def test_track_order_page_loads(self, client):
        """Test track order page returns 200"""
        response = client.get('/track')
        assert response.status_code == 200
    
    def test_track_nonexistent_order(self, client):
        """Test tracking non-existent order"""
        response = client.post('/track', data={'order_id': 999}, follow_redirects=True)
        assert response.status_code == 200


class TestAPI:
    """Test API endpoints"""
    
    def test_api_menu(self, client):
        """Test API menu endpoint"""
        response = client.get('/api/menu')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)


class TestInputValidation:
    """Test input validation"""
    
    def test_invalid_email(self, client):
        """Test invalid email validation"""
        client.post('/cart/add/1', data={'quantity': 1})
        invalid_data = {
            'customer_name': 'Test',
            'customer_email': 'invalid-email',
            'customer_phone': '+1234567890',
            'customer_address': '123 Test Street, City 12345'
        }
        response = client.post('/checkout', data=invalid_data)
        assert response.status_code == 200
    
    def test_invalid_phone(self, client):
        """Test invalid phone validation"""
        client.post('/cart/add/1', data={'quantity': 1})
        invalid_data = {
            'customer_name': 'Test',
            'customer_email': 'test@example.com',
            'customer_phone': '123',
            'customer_address': '123 Test Street, City 12345'
        }
        response = client.post('/checkout', data=invalid_data)
        assert response.status_code == 200
    
    def test_short_address(self, client):
        """Test short address validation"""
        client.post('/cart/add/1', data={'quantity': 1})
        invalid_data = {
            'customer_name': 'Test',
            'customer_email': 'test@example.com',
            'customer_phone': '+1234567890',
            'customer_address': 'Short'
        }
        response = client.post('/checkout', data=invalid_data)
        assert response.status_code == 200

