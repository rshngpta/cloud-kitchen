from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db, MenuItem, Order, OrderItem
from forms import MenuItemForm, OrderForm, PaymentForm
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize database
db.init_app(app)

# Create tables on first request
with app.app_context():
    db.create_all()
    # Add sample menu items if database is empty
    if MenuItem.query.count() == 0:
        sample_items = [
            MenuItem(name='Spring Rolls', description='Crispy vegetable spring rolls', price=5.99, category='starters'),
            MenuItem(name='Chicken Tikka', description='Grilled chicken with spices', price=12.99, category='main_course'),
            MenuItem(name='Butter Chicken', description='Creamy tomato-based chicken curry', price=14.99, category='main_course'),
            MenuItem(name='Vegetable Biryani', description='Aromatic rice with mixed vegetables', price=10.99, category='main_course'),
            MenuItem(name='Chocolate Brownie', description='Rich chocolate brownie with ice cream', price=6.99, category='desserts'),
            MenuItem(name='Mango Lassi', description='Sweet mango yogurt drink', price=3.99, category='beverages'),
        ]
        db.session.add_all(sample_items)
        db.session.commit()


# ==================== HOME ====================
@app.route('/')
def home():
    """Home page"""
    return render_template('home.html')


# ==================== MENU CRUD ====================
@app.route('/menu')
def menu():
    """Display all menu items (Read)"""
    category = request.args.get('category', 'all')
    if category == 'all':
        items = MenuItem.query.filter_by(available=True).all()
    else:
        items = MenuItem.query.filter_by(category=category, available=True).all()
    return render_template('menu.html', items=items, category=category)


@app.route('/admin/menu')
def admin_menu():
    """Admin view of all menu items"""
    items = MenuItem.query.all()
    return render_template('admin_menu.html', items=items)


@app.route('/admin/menu/add', methods=['GET', 'POST'])
def add_menu_item():
    """Add new menu item (Create)"""
    form = MenuItemForm()
    if form.validate_on_submit():
        item = MenuItem(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            available=form.available.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Menu item added successfully!', 'success')
        return redirect(url_for('admin_menu'))
    return render_template('menu_form.html', form=form, title='Add Menu Item')


@app.route('/admin/menu/edit/<int:id>', methods=['GET', 'POST'])
def edit_menu_item(id):
    """Edit menu item (Update)"""
    item = MenuItem.query.get_or_404(id)
    form = MenuItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.price = form.price.data
        item.category = form.category.data
        item.available = form.available.data
        db.session.commit()
        flash('Menu item updated successfully!', 'success')
        return redirect(url_for('admin_menu'))
    return render_template('menu_form.html', form=form, title='Edit Menu Item')


@app.route('/admin/menu/delete/<int:id>', methods=['POST'])
def delete_menu_item(id):
    """Delete menu item (Delete)"""
    item = MenuItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Menu item deleted successfully!', 'success')
    return redirect(url_for('admin_menu'))


# ==================== CART ====================
@app.route('/cart')
def cart():
    """View cart"""
    cart_items = session.get('cart', {})
    items = []
    total = 0
    for item_id, quantity in cart_items.items():
        menu_item = MenuItem.query.get(int(item_id))
        if menu_item:
            subtotal = menu_item.price * quantity
            items.append({
                'id': menu_item.id,
                'name': menu_item.name,
                'price': menu_item.price,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
    return render_template('cart.html', items=items, total=total)


@app.route('/cart/add/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    """Add item to cart"""
    quantity = int(request.form.get('quantity', 1))
    if quantity < 1:
        flash('Invalid quantity', 'error')
        return redirect(url_for('menu'))
    
    cart = session.get('cart', {})
    item_key = str(item_id)
    
    if item_key in cart:
        cart[item_key] += quantity
    else:
        cart[item_key] = quantity
    
    session['cart'] = cart
    flash('Item added to cart!', 'success')
    return redirect(url_for('menu'))


@app.route('/cart/update/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    """Update cart item quantity"""
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    item_key = str(item_id)
    
    if quantity > 0:
        cart[item_key] = quantity
    else:
        cart.pop(item_key, None)
    
    session['cart'] = cart
    flash('Cart updated!', 'success')
    return redirect(url_for('cart'))


@app.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    """Remove item from cart"""
    cart = session.get('cart', {})
    cart.pop(str(item_id), None)
    session['cart'] = cart
    flash('Item removed from cart!', 'success')
    return redirect(url_for('cart'))


@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    """Clear entire cart"""
    session['cart'] = {}
    flash('Cart cleared!', 'success')
    return redirect(url_for('cart'))


# ==================== CHECKOUT & ORDERS ====================
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout process"""
    cart_items = session.get('cart', {})
    if not cart_items:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('menu'))
    
    form = OrderForm()
    
    # Calculate total
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
        # Store order details in session for payment
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
    """Payment processing"""
    order_details = session.get('order_details')
    cart_items = session.get('cart', {})
    
    if not order_details or not cart_items:
        flash('Please complete checkout first!', 'error')
        return redirect(url_for('checkout'))
    
    form = PaymentForm()
    
    if form.validate_on_submit():
        # Create order
        order = Order(
            customer_name=order_details['customer_name'],
            customer_email=order_details['customer_email'],
            customer_phone=order_details['customer_phone'],
            customer_address=order_details['customer_address'],
            total_amount=order_details['total'],
            payment_method=form.payment_method.data,
            status='confirmed',
            payment_status='paid' if form.payment_method.data == 'card' else 'pending'
        )
        db.session.add(order)
        db.session.flush()
        
        # Add order items
        for item_id, quantity in cart_items.items():
            menu_item = MenuItem.query.get(int(item_id))
            if menu_item:
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=menu_item.id,
                    quantity=quantity,
                    price=menu_item.price
                )
                db.session.add(order_item)
        
        db.session.commit()
        
        # Clear cart and order details
        session.pop('cart', None)
        session.pop('order_details', None)
        
        flash(f'Order placed successfully! Order ID: {order.id}', 'success')
        return redirect(url_for('order_confirmation', order_id=order.id))
    
    return render_template('payment.html', form=form, total=order_details['total'])


@app.route('/order/confirmation/<int:order_id>')
def order_confirmation(order_id):
    """Order confirmation page"""
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)


# ==================== ORDER MANAGEMENT ====================
@app.route('/orders')
def orders():
    """View all orders (Admin)"""
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=all_orders)


@app.route('/order/<int:order_id>')
def order_detail(order_id):
    """View order details"""
    order = Order.query.get_or_404(order_id)
    return render_template('order_detail.html', order=order)


@app.route('/order/update/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    """Update order status"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status in ['pending', 'confirmed', 'preparing', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash('Order status updated!', 'success')
    return redirect(url_for('order_detail', order_id=order_id))


@app.route('/order/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    """Delete order"""
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted!', 'success')
    return redirect(url_for('orders'))


# ==================== TRACK ORDER ====================
@app.route('/track', methods=['GET', 'POST'])
def track_order():
    """Track order by ID"""
    order = None
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        if order_id:
            order = Order.query.get(int(order_id))
            if not order:
                flash('Order not found!', 'error')
    return render_template('track_order.html', order=order)


# ==================== API ENDPOINTS ====================
@app.route('/api/menu')
def api_menu():
    """API endpoint for menu items"""
    items = MenuItem.query.filter_by(available=True).all()
    return jsonify([item.to_dict() for item in items])


@app.route('/api/order/<int:order_id>')
def api_order(order_id):
    """API endpoint for order details"""
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict())


# ==================== HEALTH CHECK ====================
@app.route('/health')
def health():
    """Health check endpoint for CI/CD"""
    return jsonify({'status': 'healthy', 'app': 'Cloud Kitchen'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', 'False') == 'True')

