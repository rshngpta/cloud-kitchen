from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError
import re


def validate_phone(form, field):
    """Custom phone number validator"""
    phone_pattern = re.compile(r'^\+?[\d\s\-]{10,15}$')
    if not phone_pattern.match(field.data):
        raise ValidationError('Invalid phone number format')


class MenuItemForm(FlaskForm):
    """Form for creating/updating menu items with validation"""
    name = StringField('Name', validators=[
        DataRequired(message='Item name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    description = TextAreaField('Description', validators=[
        Length(max=500, message='Description cannot exceed 500 characters')
    ])
    price = FloatField('Price', validators=[
        DataRequired(message='Price is required'),
        NumberRange(min=0.01, max=10000, message='Price must be between 0.01 and 10000')
    ])
    category = SelectField('Category', choices=[
        ('starters', 'Starters'),
        ('main_course', 'Main Course'),
        ('desserts', 'Desserts'),
        ('beverages', 'Beverages')
    ], validators=[DataRequired(message='Category is required')])
    available = BooleanField('Available', default=True)


class OrderForm(FlaskForm):
    """Form for placing orders with input validation"""
    customer_name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    customer_email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    customer_phone = StringField('Phone', validators=[
        DataRequired(message='Phone number is required'),
        validate_phone
    ])
    customer_address = TextAreaField('Delivery Address', validators=[
        DataRequired(message='Delivery address is required'),
        Length(min=10, max=500, message='Address must be between 10 and 500 characters')
    ])


class PaymentForm(FlaskForm):
    """Form for payment processing with validation"""
    payment_method = SelectField('Payment Method', choices=[
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash on Delivery')
    ], validators=[DataRequired(message='Please select a payment method')])
    card_number = StringField('Card Number', validators=[
        Length(max=19, message='Invalid card number')
    ])
    card_expiry = StringField('Expiry (MM/YY)', validators=[
        Length(max=5, message='Invalid expiry format')
    ])
    card_cvv = StringField('CVV', validators=[
        Length(max=4, message='Invalid CVV')
    ])

