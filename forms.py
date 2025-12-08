"""
Cloud Kitchen - Form Definitions Module
=======================================
Author: [Your Name]
Date: December 2025
Module: H9CDOS - Cloud DevOps

Description:
    This module defines WTForms form classes for the Cloud Kitchen application.
    Forms provide server-side validation for all user inputs, ensuring data
    integrity and security.

Security Features:
    - CSRF protection via Flask-WTF
    - Input validation and sanitization
    - Custom validators for phone numbers
    - Length limits to prevent buffer overflow attacks

Technology:
    - Flask-WTF: Flask integration for WTForms
    - WTForms: Python form validation library
"""

# ==============================================================================
# IMPORTS
# ==============================================================================
from flask_wtf import FlaskForm  # Base class for Flask forms with CSRF
from wtforms import (
    StringField,      # Text input fields
    FloatField,       # Numeric decimal input
    TextAreaField,    # Multi-line text input
    SelectField,      # Dropdown selection
    IntegerField,     # Integer input
    BooleanField      # Checkbox input
)
from wtforms.validators import (
    DataRequired,     # Field cannot be empty
    Email,            # Must be valid email format
    Length,           # Min/max character length
    NumberRange,      # Min/max numeric value
    ValidationError   # Custom validation error
)
import re  # Regular expressions for custom validation


# ==============================================================================
# CUSTOM VALIDATORS
# ==============================================================================

def validate_phone(form, field):
    """
    Custom Phone Number Validator
    -----------------------------
    Validates phone numbers against a flexible international format.
    
    Accepted Formats:
        - +1234567890 (international with plus)
        - 1234567890 (10 digits minimum)
        - 123-456-7890 (with dashes)
        - 123 456 7890 (with spaces)
    
    Parameters:
        form: The form instance (not used but required by WTForms)
        field: The field being validated
    
    Raises:
        ValidationError: If phone number doesn't match expected pattern
    
    Example:
        >>> validate_phone(form, field_with_value('+353891234567'))
        # Passes validation
        >>> validate_phone(form, field_with_value('abc'))
        # Raises ValidationError
    """
    # Regex pattern explanation:
    # ^          - Start of string
    # \+?        - Optional plus sign for international format
    # [\d\s\-]   - Digits, spaces, or dashes
    # {10,15}    - Between 10 and 15 characters
    # $          - End of string
    phone_pattern = re.compile(r'^\+?[\d\s\-]{10,15}$')
    
    if not phone_pattern.match(field.data):
        raise ValidationError('Invalid phone number format')


# ==============================================================================
# MENU ITEM FORM
# ==============================================================================

class MenuItemForm(FlaskForm):
    """
    Menu Item Form - For Creating and Editing Menu Items
    ====================================================
    
    This form is used in the admin panel for managing menu items.
    It provides validation for all menu item fields.
    
    Fields:
        name: Item name (2-100 characters, required)
        description: Detailed description (up to 500 characters)
        price: Item price (0.01 - 10000, required)
        category: Item category (dropdown, required)
        available: Availability status (checkbox)
    
    Usage:
        # In route handler
        form = MenuItemForm()
        if form.validate_on_submit():
            # Process valid form data
            name = form.name.data
    """
    
    # Name field with length validation
    name = StringField('Name', validators=[
        DataRequired(message='Item name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    # Description field - optional but length limited
    description = TextAreaField('Description', validators=[
        Length(max=500, message='Description cannot exceed 500 characters')
    ])
    
    # Price field with range validation
    # Prevents negative prices and unreasonably high values
    price = FloatField('Price', validators=[
        DataRequired(message='Price is required'),
        NumberRange(min=0.01, max=10000, message='Price must be between 0.01 and 10000')
    ])
    
    # Category dropdown - predefined choices ensure data consistency
    category = SelectField('Category', choices=[
        ('starters', 'Starters'),
        ('main_course', 'Main Course'),
        ('desserts', 'Desserts'),
        ('beverages', 'Beverages')
    ], validators=[DataRequired(message='Category is required')])
    
    # Availability checkbox - defaults to True (available)
    available = BooleanField('Available', default=True)


# ==============================================================================
# ORDER FORM
# ==============================================================================

class OrderForm(FlaskForm):
    """
    Order Form - Customer Details for Checkout
    ==========================================
    
    This form collects customer information during the checkout process.
    All fields are required for successful order processing and delivery.
    
    Fields:
        customer_name: Full name (2-100 characters)
        customer_email: Valid email address
        customer_phone: Phone number (custom validation)
        customer_address: Delivery address (10-500 characters)
    
    Validation:
        - Email format validation using wtforms Email validator
        - Phone validation using custom regex validator
        - Address minimum length ensures usable delivery info
    
    Usage:
        form = OrderForm()
        if form.validate_on_submit():
            name = form.customer_name.data
            email = form.customer_email.data
    """
    
    # Customer name - required with length limits
    customer_name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    # Email field with format validation
    # Email validator checks for @ symbol and domain format
    customer_email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    
    # Phone field with custom validator
    customer_phone = StringField('Phone', validators=[
        DataRequired(message='Phone number is required'),
        validate_phone  # Custom validator function defined above
    ])
    
    # Delivery address - minimum length ensures useful address
    customer_address = TextAreaField('Delivery Address', validators=[
        DataRequired(message='Delivery address is required'),
        Length(min=10, max=500, message='Address must be between 10 and 500 characters')
    ])


# ==============================================================================
# PAYMENT FORM
# ==============================================================================

class PaymentForm(FlaskForm):
    """
    Payment Form - Payment Method Selection
    =======================================
    
    This form handles payment method selection during checkout.
    Card details are validated but actual payment processing would
    require integration with a payment gateway (Stripe, PayPal, etc.)
    
    Fields:
        payment_method: Card or Cash on Delivery
        card_number: Credit/Debit card number (optional)
        card_expiry: Expiration date MM/YY format
        card_cvv: Security code (3-4 digits)
    
    Note:
        In a production environment, card details should be handled
        by a PCI-compliant payment processor, not stored locally.
    
    Security:
        - Card fields have length limits to prevent injection
        - Actual card processing should use tokenization
    
    Usage:
        form = PaymentForm()
        if form.validate_on_submit():
            method = form.payment_method.data
            if method == 'card':
                # Process card payment via payment gateway
                pass
    """
    
    # Payment method dropdown
    payment_method = SelectField('Payment Method', choices=[
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash on Delivery')
    ], validators=[DataRequired(message='Please select a payment method')])
    
    # Card number field - optional (only required for card payment)
    # In production, this would be handled by a payment gateway iframe
    card_number = StringField('Card Number', validators=[
        Length(max=19, message='Invalid card number')  # 16 digits + 3 spaces
    ])
    
    # Expiry date in MM/YY format
    card_expiry = StringField('Expiry (MM/YY)', validators=[
        Length(max=5, message='Invalid expiry format')  # MM/YY = 5 chars
    ])
    
    # CVV/CVC security code
    card_cvv = StringField('CVV', validators=[
        Length(max=4, message='Invalid CVV')  # 3-4 digits depending on card type
    ])
