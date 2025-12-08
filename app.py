"""
Cloud Kitchen - Main Application Module
========================================
Author: [Your Name]
Date: December 2025
Module: H9CDOS - Cloud DevOps

Description:
    This is the main Flask application file for the Cloud Kitchen food ordering system.
    It implements a complete CRUD (Create, Read, Update, Delete) functionality for
    menu items and orders, along with shopping cart management and payment processing.

Features:
    - Menu management with full CRUD operations
    - Shopping cart functionality using Flask sessions
    - Order processing and tracking
    - RESTful API endpoints for integration
    - Health check endpoint for CI/CD pipeline monitoring

Technology Stack:
    - Flask: Web framework
    - SQLAlchemy: ORM for database operations
    - Flask-WTF: Form handling with CSRF protection
    - Jinja2: Template rendering
"""

# ==============================================================================
# IMPORTS
# ==============================================================================
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf.csrf import CSRFProtect  # Cross-Site Request Forgery protection
from config import Config  # Application configuration settings
from models import db, MenuItem, Order, OrderItem  # Database models
from forms import MenuItemForm, OrderForm, PaymentForm  # Form validation classes
import os  # Operating system interface for environment variables

# ==============================================================================
# APPLICATION INITIALIZATION
# ==============================================================================

# Create Flask application instance
# __name__ helps Flask determine the root path of the application
app = Flask(__name__)

# Load configuration from Config class
# This includes SECRET_KEY, DATABASE_URI, and other settings
app.config.from_object(Config)

# Initialize CSRF (Cross-Site Request Forgery) protection
# This adds security tokens to forms to prevent malicious submissions
csrf = CSRFProtect(app)

# Initialize SQLAlchemy database connection
# db.init_app() binds the database instance to this Flask application
db.init_app(app)

# ==============================================================================
# DATABASE INITIALIZATION AND SEEDING
# ==============================================================================

# Create database tables and seed with sample data
# app.app_context() ensures database operations have access to app configuration
with app.app_context():
    # Create all database tables defined in models.py
    # This is equivalent to running migrations
    db.create_all()
    
    # Check if database is empty and seed with sample menu items
    # This ensures the application has data for demonstration purposes
    if MenuItem.query.count() == 0:
        # Define sample menu items for each category
        sample_items = [
            # Starters category
            MenuItem(name='Spring Rolls', description='Crispy vegetable spring rolls', 
                    price=5.99, category='starters'),
            # Main course items
            MenuItem(name='Chicken Tikka', description='Grilled chicken with spices', 
                    price=12.99, category='main_course'),
            MenuItem(name='Butter Chicken', description='Creamy tomato-based chicken curry', 
                    price=14.99, category='main_course'),
            MenuItem(name='Vegetable Biryani', description='Aromatic rice with mixed vegetables', 
                    price=10.99, category='main_course'),
            # Desserts category
            MenuItem(name='Chocolate Brownie', description='Rich chocolate brownie with ice cream', 
                    price=6.99, category='desserts'),
            # Beverages category
            MenuItem(name='Mango Lassi', description='Sweet mango yogurt drink', 
                    price=3.99, category='beverages'),
        ]
        # Add all items to the session and commit to database
        db.session.add_all(sample_items)
        db.session.commit()


# ==============================================================================
# HOME ROUTE
# ==============================================================================

@app.route('/')
def home():
    """
    Home Page Route
    ---------------
    Renders the landing page of the Cloud Kitchen application.
    
    Returns:
        HTML template: home.html with navigation and welcome content
    """
    return render_template('home.html')


# ==============================================================================
# MENU CRUD OPERATIONS
# ==============================================================================

@app.route('/menu')
def menu():
    """
    Menu Display Route (READ operation)
    ------------------------------------
    Displays all available menu items, optionally filtered by category.
    
    Query Parameters:
        category (str): Filter items by category ('all', 'starters', 'main_course', etc.)
    
    Returns:
        HTML template: menu.html with filtered menu items
    """
    # Get category filter from URL query parameters, default to 'all'
    category = request.args.get('category', 'all')
    
    # Query database based on category filter
    if category == 'all':
        # Get all available items regardless of category
        items = MenuItem.query.filter_by(available=True).all()
    else:
        # Filter by specific category and availability
        items = MenuItem.query.filter_by(category=category, available=True).all()
    
    return render_template('menu.html', items=items, category=category)


@app.route('/admin/menu')
def admin_menu():
    """
    Admin Menu Management Route
    ---------------------------
    Displays all menu items (including unavailable) for administrative management.
    
    Returns:
        HTML template: admin_menu.html with all menu items and CRUD controls
    """
    # Query all items without filtering by availability
    items = MenuItem.query.all()
    return render_template('admin_menu.html', items=items)


@app.route('/admin/menu/add', methods=['GET', 'POST'])
def add_menu_item():
    """
    Add New Menu Item Route (CREATE operation)
    ------------------------------------------
    Handles both displaying the form (GET) and processing form submission (POST).
    
    Methods:
        GET: Display empty form for new menu item
        POST: Validate and save new menu item to database
    
    Returns:
        GET: HTML form template
        POST: Redirect to admin menu on success, or form with errors
    """
    # Create form instance for menu item
    form = MenuItemForm()
    
    # validate_on_submit() checks if form was submitted via POST
    # and all validators passed
    if form.validate_on_submit():
        # Create new MenuItem object from form data
        item = MenuItem(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            available=form.available.data
        )
        # Add to database session and commit
        db.session.add(item)
        db.session.commit()
        
        # Flash success message and redirect
        flash('Menu item added successfully!', 'success')
        return redirect(url_for('admin_menu'))
    
    # Render form template (GET request or validation failed)
    return render_template('menu_form.html', form=form, title='Add Menu Item')


@app.route('/admin/menu/edit/<int:id>', methods=['GET', 'POST'])
def edit_menu_item(id):
    """
    Edit Menu Item Route (UPDATE operation)
    ---------------------------------------
    Handles updating existing menu items.
    
    Parameters:
        id (int): The database ID of the menu item to edit
    
    Methods:
        GET: Display form pre-filled with existing data
        POST: Validate and update menu item in database
    
    Returns:
        GET: HTML form template with existing data
        POST: Redirect to admin menu on success
    """
    # Query item by ID, return 404 if not found
    item = MenuItem.query.get_or_404(id)
    
    # Create form and populate with existing item data
    form = MenuItemForm(obj=item)
    
    if form.validate_on_submit():
        # Update item attributes from form data
        item.name = form.name.data
        item.description = form.description.data
        item.price = form.price.data
        item.category = form.category.data
        item.available = form.available.data
        
        # Commit changes to database
        db.session.commit()
        flash('Menu item updated successfully!', 'success')
        return redirect(url_for('admin_menu'))
    
    return render_template('menu_form.html', form=form, title='Edit Menu Item')


@app.route('/admin/menu/delete/<int:id>', methods=['POST'])
def delete_menu_item(id):
    """
    Delete Menu Item Route (DELETE operation)
    -----------------------------------------
    Removes a menu item from the database.
    
    Parameters:
        id (int): The database ID of the menu item to delete
    
    Methods:
        POST: Only accepts POST requests for security (prevents accidental deletion via URL)
    
    Returns:
        Redirect to admin menu with success message
    """
    # Query item by ID, return 404 if not found
    item = MenuItem.query.get_or_404(id)
    
    # Delete from database and commit
    db.session.delete(item)
    db.session.commit()
    
    flash('Menu item deleted successfully!', 'success')
    return redirect(url_for('admin_menu'))


# ==============================================================================
# SHOPPING CART OPERATIONS
# ==============================================================================

@app.route('/cart')
def cart():
    """
    View Shopping Cart Route
    ------------------------
    Displays all items currently in the user's shopping cart.
    Cart data is stored in Flask session (client-side cookies).
    
    Returns:
        HTML template: cart.html with cart items, quantities, and total
    """
    # Retrieve cart from session, default to empty dict
    cart_items = session.get('cart', {})
    items = []
    total = 0
    
    # Build cart display data
    for item_id, quantity in cart_items.items():
        # Get menu item details from database
        menu_item = MenuItem.query.get(int(item_id))
        if menu_item:
            # Calculate subtotal for this item
            subtotal = menu_item.price * quantity
            items.append({
                'id': menu_item.id,
                'name': menu_item.name,
                'price': menu_item.price,
                'quantity': quantity,
                'subtotal': subtotal
            })
            # Accumulate total
            total += subtotal
    
    return render_template('cart.html', items=items, total=total)


@app.route('/cart/add/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    """
    Add Item to Cart Route
    ----------------------
    Adds a menu item to the shopping cart with specified quantity.
    
    Parameters:
        item_id (int): The database ID of the menu item to add
    
    Form Data:
        quantity (int): Number of items to add (default: 1)
    
    Returns:
        Redirect to menu page with success/error message
    """
    # Get quantity from form, default to 1
    quantity = int(request.form.get('quantity', 1))
    
    # Validate quantity
    if quantity < 1:
        flash('Invalid quantity', 'error')
        return redirect(url_for('menu'))
    
    # Get current cart from session
    cart = session.get('cart', {})
    item_key = str(item_id)  # Session keys must be strings
    
    # Add to existing quantity or create new entry
    if item_key in cart:
        cart[item_key] += quantity
    else:
        cart[item_key] = quantity
    
    # Save updated cart back to session
    session['cart'] = cart
    flash('Item added to cart!', 'success')
    return redirect(url_for('menu'))


@app.route('/cart/update/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    """
    Update Cart Item Quantity Route
    -------------------------------
    Updates the quantity of an existing cart item.
    If quantity is 0 or less, removes the item from cart.
    
    Parameters:
        item_id (int): The database ID of the menu item to update
    
    Form Data:
        quantity (int): New quantity value
    
    Returns:
        Redirect to cart page with success message
    """
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    item_key = str(item_id)
    
    # Update or remove based on quantity
    if quantity > 0:
        cart[item_key] = quantity
    else:
        # Remove item if quantity is 0 or negative
        cart.pop(item_key, None)
    
    session['cart'] = cart
    flash('Cart updated!', 'success')
    return redirect(url_for('cart'))


@app.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    """
    Remove Item from Cart Route
    ---------------------------
    Completely removes an item from the shopping cart.
    
    Parameters:
        item_id (int): The database ID of the menu item to remove
    
    Returns:
        Redirect to cart page with success message
    """
    cart = session.get('cart', {})
    # Remove item, pop() returns None if key doesn't exist
    cart.pop(str(item_id), None)
    session['cart'] = cart
    flash('Item removed from cart!', 'success')
    return redirect(url_for('cart'))


@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    """
    Clear Entire Cart Route
    -----------------------
    Removes all items from the shopping cart.
    
    Returns:
        Redirect to cart page with success message
    """
    session['cart'] = {}
    flash('Cart cleared!', 'success')
    return redirect(url_for('cart'))


# ==============================================================================
# CHECKOUT AND ORDER PROCESSING
# ==============================================================================

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """
    Checkout Process Route
    ----------------------
    Handles the checkout process where customers enter delivery details.
    
    Methods:
        GET: Display checkout form with cart summary
        POST: Validate customer details and proceed to payment
    
    Returns:
        GET: HTML checkout form with cart items and total
        POST: Redirect to payment page on success
    """
    # Verify cart is not empty
    cart_items = session.get('cart', {})
    if not cart_items:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('menu'))
    
    form = OrderForm()
    
    # Build cart summary with totals
    items = []
    total = 0
    for item_id, quantity in cart_items.items():
        menu_item = MenuItem.query.get(int(item_id))
        if menu_item:
            subtotal = menu_item.price * quantity
            items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    if form.validate_on_submit():
        # Store validated order details in session for payment step
        session['order_details'] = {
            'customer_name': form.customer_name.data,
            'customer_email': form.customer_email.data,
            'customer_phone': form.customer_phone.data,
            'customer_address': form.customer_address.data,
            'total': total
        }
        return redirect(url_for('payment'))
    
    return render_template('checkout.html', form=form, items=items, total=total)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    """
    Payment Processing Route
    ------------------------
    Handles payment method selection and order finalization.
    Creates order record and order items in the database.
    
    Methods:
        GET: Display payment form
        POST: Process payment and create order
    
    Returns:
        GET: HTML payment form
        POST: Redirect to order confirmation on success
    """
    # Retrieve order details and cart from session
    order_details = session.get('order_details')
    cart_items = session.get('cart', {})
    
    # Verify checkout was completed
    if not order_details or not cart_items:
        flash('Please complete checkout first!', 'error')
        return redirect(url_for('checkout'))
    
    form = PaymentForm()
    
    if form.validate_on_submit():
        # Create new Order record
        order = Order(
            customer_name=order_details['customer_name'],
            customer_email=order_details['customer_email'],
            customer_phone=order_details['customer_phone'],
            customer_address=order_details['customer_address'],
            total_amount=order_details['total'],
            payment_method=form.payment_method.data,
            status='confirmed',
            # Card payments are marked as paid immediately
            payment_status='paid' if form.payment_method.data == 'card' else 'pending'
        )
        db.session.add(order)
        # flush() assigns ID without committing, needed for foreign key
        db.session.flush()
        
        # Create OrderItem records for each cart item
        for item_id, quantity in cart_items.items():
            menu_item = MenuItem.query.get(int(item_id))
            if menu_item:
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=menu_item.id,
                    quantity=quantity,
                    price=menu_item.price  # Store price at time of order
                )
                db.session.add(order_item)
        
        # Commit all changes to database
        db.session.commit()
        
        # Clear cart and order details from session
        session.pop('cart', None)
        session.pop('order_details', None)
        
        flash(f'Order placed successfully! Order ID: {order.id}', 'success')
        return redirect(url_for('order_confirmation', order_id=order.id))
    
    return render_template('payment.html', form=form, total=order_details['total'])


@app.route('/order/confirmation/<int:order_id>')
def order_confirmation(order_id):
    """
    Order Confirmation Route
    ------------------------
    Displays order confirmation details after successful payment.
    
    Parameters:
        order_id (int): The database ID of the completed order
    
    Returns:
        HTML template: order_confirmation.html with order details
    """
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)


# ==============================================================================
# ORDER MANAGEMENT (ADMIN)
# ==============================================================================

@app.route('/orders')
def orders():
    """
    View All Orders Route (Admin)
    -----------------------------
    Displays all orders in the system for administrative management.
    Orders are sorted by creation date (newest first).
    
    Returns:
        HTML template: orders.html with all orders
    """
    # Query all orders, ordered by creation date descending
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=all_orders)


@app.route('/order/<int:order_id>')
def order_detail(order_id):
    """
    View Order Details Route
    ------------------------
    Displays detailed information about a specific order.
    
    Parameters:
        order_id (int): The database ID of the order
    
    Returns:
        HTML template: order_detail.html with full order information
    """
    order = Order.query.get_or_404(order_id)
    return render_template('order_detail.html', order=order)


@app.route('/order/update/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    """
    Update Order Status Route
    -------------------------
    Updates the status of an order (e.g., pending -> confirmed -> delivered).
    
    Parameters:
        order_id (int): The database ID of the order to update
    
    Form Data:
        status (str): New status value
    
    Valid Status Values:
        - pending: Order received
        - confirmed: Order confirmed
        - preparing: Being prepared
        - delivered: Delivered to customer
        - cancelled: Order cancelled
    
    Returns:
        Redirect to order detail page with success message
    """
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    # Validate status value
    valid_statuses = ['pending', 'confirmed', 'preparing', 'delivered', 'cancelled']
    if new_status in valid_statuses:
        order.status = new_status
        db.session.commit()
        flash('Order status updated!', 'success')
    
    return redirect(url_for('order_detail', order_id=order_id))


@app.route('/order/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    """
    Delete Order Route
    ------------------
    Removes an order and its associated items from the database.
    Cascade delete is handled by the model relationship.
    
    Parameters:
        order_id (int): The database ID of the order to delete
    
    Returns:
        Redirect to orders list with success message
    """
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted!', 'success')
    return redirect(url_for('orders'))


# ==============================================================================
# ORDER TRACKING (CUSTOMER)
# ==============================================================================

@app.route('/track', methods=['GET', 'POST'])
def track_order():
    """
    Track Order Route
    -----------------
    Allows customers to track their order status using order ID.
    
    Methods:
        GET: Display tracking form
        POST: Look up order and display status
    
    Form Data:
        order_id (int): The order ID to track
    
    Returns:
        HTML template: track_order.html with order details (if found)
    """
    order = None
    
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        if order_id:
            # Look up order by ID
            order = Order.query.get(int(order_id))
            if not order:
                flash('Order not found!', 'error')
    
    return render_template('track_order.html', order=order)


# ==============================================================================
# REST API ENDPOINTS
# ==============================================================================

@app.route('/api/menu')
def api_menu():
    """
    API: Get Menu Items
    -------------------
    RESTful endpoint returning all available menu items as JSON.
    Useful for mobile apps or third-party integrations.
    
    Returns:
        JSON array of menu item objects
    
    Example Response:
        [
            {"id": 1, "name": "Spring Rolls", "price": 5.99, ...},
            {"id": 2, "name": "Chicken Tikka", "price": 12.99, ...}
        ]
    """
    items = MenuItem.query.filter_by(available=True).all()
    return jsonify([item.to_dict() for item in items])


@app.route('/api/order/<int:order_id>')
def api_order(order_id):
    """
    API: Get Order Details
    ----------------------
    RESTful endpoint returning order details as JSON.
    
    Parameters:
        order_id (int): The database ID of the order
    
    Returns:
        JSON object with order details and items
    
    Example Response:
        {
            "id": 1,
            "customer_name": "John Doe",
            "total_amount": 25.99,
            "status": "confirmed",
            "items": [...]
        }
    """
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict())


# ==============================================================================
# HEALTH CHECK ENDPOINT (CI/CD)
# ==============================================================================

@app.route('/health')
def health():
    """
    Health Check Endpoint
    ---------------------
    Simple endpoint for CI/CD pipeline and load balancer health checks.
    Returns JSON with application status.
    
    Used by:
        - Jenkins pipeline for deployment verification
        - AWS Elastic Beanstalk for instance health monitoring
        - Docker container health checks
    
    Returns:
        JSON: {"status": "healthy", "app": "Cloud Kitchen"}
    """
    return jsonify({'status': 'healthy', 'app': 'Cloud Kitchen'})


# ==============================================================================
# APPLICATION ENTRY POINT
# ==============================================================================

if __name__ == '__main__':
    """
    Development Server Entry Point
    ------------------------------
    This block only runs when executing the script directly (not via Gunicorn).
    Used for local development and testing.
    
    Environment Variables:
        PORT: Server port (default: 5000)
        DEBUG: Enable debug mode (default: False)
    """
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run Flask development server
    # host='0.0.0.0' makes server accessible externally
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', 'False') == 'True')
