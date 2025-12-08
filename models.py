"""
Cloud Kitchen - Database Models Module
======================================
Author: [Your Name]
Date: December 2025
Module: H9CDOS - Cloud DevOps

Description:
    This module defines the SQLAlchemy ORM models for the Cloud Kitchen application.
    It implements three main entities: MenuItem, Order, and OrderItem.
    
    The models follow database normalization principles with proper relationships
    and foreign key constraints for data integrity.

Database Schema:
    - menu_items: Stores food items available for ordering
    - orders: Stores customer orders with delivery details
    - order_items: Junction table linking orders to menu items (many-to-many)

Technology:
    - SQLAlchemy: Python ORM for database abstraction
    - Flask-SQLAlchemy: Flask integration for SQLAlchemy
"""

# ==============================================================================
# IMPORTS
# ==============================================================================
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy ORM integration for Flask
from datetime import datetime  # For timestamp handling

# ==============================================================================
# DATABASE INSTANCE
# ==============================================================================

# Create SQLAlchemy database instance
# This will be initialized with the Flask app in app.py using db.init_app(app)
db = SQLAlchemy()


# ==============================================================================
# MENU ITEM MODEL
# ==============================================================================

class MenuItem(db.Model):
    """
    MenuItem Model - Represents food items in the menu
    ==================================================
    
    This model stores all menu items available for ordering.
    It supports CRUD operations through the admin interface.
    
    Attributes:
        id (int): Primary key, auto-incremented
        name (str): Name of the food item (required, max 100 chars)
        description (str): Detailed description (optional, max 500 chars)
        price (float): Price in currency units (required)
        category (str): Category for filtering (starters, main_course, etc.)
        available (bool): Whether item is currently available
        created_at (datetime): Timestamp when item was created
        updated_at (datetime): Timestamp of last update
    
    Example:
        >>> item = MenuItem(name='Pizza', price=12.99, category='main_course')
        >>> db.session.add(item)
        >>> db.session.commit()
    """
    
    # Define the database table name
    __tablename__ = 'menu_items'
    
    # Primary key - unique identifier for each menu item
    id = db.Column(db.Integer, primary_key=True)
    
    # Name of the food item - required field
    name = db.Column(db.String(100), nullable=False)
    
    # Description - optional detailed information about the item
    description = db.Column(db.String(500))
    
    # Price - stored as float for currency calculations
    price = db.Column(db.Float, nullable=False)
    
    # Category - used for menu filtering and organization
    # Valid values: 'starters', 'main_course', 'desserts', 'beverages'
    category = db.Column(db.String(50), nullable=False)
    
    # Availability flag - allows hiding items without deletion
    available = db.Column(db.Boolean, default=True)
    
    # Timestamp when record was created
    # default=datetime.utcnow is called when record is inserted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Timestamp when record was last updated
    # onupdate=datetime.utcnow automatically updates on modification
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """
        Convert MenuItem to Dictionary
        -------------------------------
        Serializes the MenuItem object to a dictionary format.
        Used for JSON API responses.
        
        Returns:
            dict: Dictionary representation of the menu item
            
        Example Output:
            {
                'id': 1,
                'name': 'Spring Rolls',
                'description': 'Crispy vegetable spring rolls',
                'price': 5.99,
                'category': 'starters',
                'available': True
            }
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'available': self.available
        }


# ==============================================================================
# ORDER MODEL
# ==============================================================================

class Order(db.Model):
    """
    Order Model - Represents customer orders
    ========================================
    
    This model stores order information including customer details,
    payment information, and order status for tracking.
    
    Attributes:
        id (int): Primary key, auto-incremented (serves as Order ID)
        customer_name (str): Full name of the customer
        customer_email (str): Email address for order confirmation
        customer_phone (str): Phone number for delivery contact
        customer_address (str): Delivery address
        total_amount (float): Total order amount
        status (str): Current order status
        payment_status (str): Payment processing status
        payment_method (str): Method of payment (card/cash)
        created_at (datetime): Order creation timestamp
        updated_at (datetime): Last update timestamp
        items (relationship): Related OrderItem objects
    
    Order Status Flow:
        pending -> confirmed -> preparing -> delivered
                              -> cancelled (at any stage)
    
    Payment Status:
        pending: Awaiting payment (cash on delivery)
        paid: Payment completed
        failed: Payment failed
    """
    
    # Define the database table name
    __tablename__ = 'orders'
    
    # Primary key - also serves as the Order ID shown to customers
    id = db.Column(db.Integer, primary_key=True)
    
    # Customer information - all required for delivery
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_address = db.Column(db.String(500), nullable=False)
    
    # Financial information
    total_amount = db.Column(db.Float, nullable=False)
    
    # Order status tracking
    # Valid values: 'pending', 'confirmed', 'preparing', 'delivered', 'cancelled'
    status = db.Column(db.String(20), default='pending')
    
    # Payment status tracking
    # Valid values: 'pending', 'paid', 'failed'
    payment_status = db.Column(db.String(20), default='pending')
    
    # Payment method
    # Valid values: 'cash', 'card'
    payment_method = db.Column(db.String(20))
    
    # Timestamps for tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to OrderItem model
    # backref='order' creates reverse relationship from OrderItem
    # lazy=True loads items only when accessed
    # cascade='all, delete-orphan' deletes items when order is deleted
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """
        Convert Order to Dictionary
        ----------------------------
        Serializes the Order object including related items.
        Used for JSON API responses.
        
        Returns:
            dict: Complete order information including items
            
        Example Output:
            {
                'id': 1,
                'customer_name': 'John Doe',
                'total_amount': 25.99,
                'status': 'confirmed',
                'items': [{'menu_item_name': 'Pizza', 'quantity': 2, ...}]
            }
        """
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'customer_address': self.customer_address,
            'total_amount': self.total_amount,
            'status': self.status,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            # Format datetime for JSON serialization
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            # Include all order items
            'items': [item.to_dict() for item in self.items]
        }


# ==============================================================================
# ORDER ITEM MODEL (JUNCTION TABLE)
# ==============================================================================

class OrderItem(db.Model):
    """
    OrderItem Model - Links Orders to Menu Items
    =============================================
    
    This is a junction table that implements the many-to-many relationship
    between Orders and MenuItems. Each record represents one line item
    in an order with quantity and price at time of purchase.
    
    Design Note:
        We store the price at time of order to preserve historical accuracy.
        Menu prices may change, but order totals should remain constant.
    
    Attributes:
        id (int): Primary key
        order_id (int): Foreign key to orders table
        menu_item_id (int): Foreign key to menu_items table
        quantity (int): Number of items ordered
        price (float): Price per item at time of order
        order (relationship): Parent Order object (via backref)
        menu_item (relationship): Related MenuItem object
    
    Example:
        >>> order_item = OrderItem(
        ...     order_id=1,
        ...     menu_item_id=5,
        ...     quantity=2,
        ...     price=12.99
        ... )
    """
    
    # Define the database table name
    __tablename__ = 'order_items'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to orders table
    # Establishes relationship to parent Order
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    
    # Foreign key to menu_items table
    # Links to the MenuItem that was ordered
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    
    # Quantity of this item in the order
    quantity = db.Column(db.Integer, nullable=False)
    
    # Price at time of order (historical record)
    # This preserves the price even if menu prices change later
    price = db.Column(db.Float, nullable=False)
    
    # Relationship to MenuItem for accessing item details
    menu_item = db.relationship('MenuItem')

    def to_dict(self):
        """
        Convert OrderItem to Dictionary
        --------------------------------
        Serializes the OrderItem with calculated subtotal.
        
        Returns:
            dict: Order item details including subtotal
            
        Example Output:
            {
                'id': 1,
                'menu_item_name': 'Spring Rolls',
                'quantity': 2,
                'price': 5.99,
                'subtotal': 11.98
            }
        """
        return {
            'id': self.id,
            # Safe access to menu_item name with fallback
            'menu_item_name': self.menu_item.name if self.menu_item else 'Unknown',
            'quantity': self.quantity,
            'price': self.price,
            # Calculate subtotal for display
            'subtotal': self.quantity * self.price
        }
