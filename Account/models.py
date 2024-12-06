from django.db import models
from django.urls import reverse
import uuid
from django.utils import timezone
import random
import os
from django.utils.html import format_html
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import string
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.timezone import now
# from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
from Products.models import Product, Brand

class MyUserManager(BaseUserManager):
    def create_user(self, mobile_number, email):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        username = email
        
        # Ensure the username is unique
        if User.objects.filter(username=username).exists():
            return {'error': 'Username already exists. Please choose another.'}
        if not mobile_number:
            raise ValueError("Users must have a mobile number")
        
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, email):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            mobile_number=mobile_number,
            email=email,

        )
        user.is_admin = True           # Admin privileges
        user.is_staff = True           # Superusers are staff
        # user.is_superuser = True       # Superuser privileges
        user.save(using=self._db)
        return user


User = get_user_model()

class UserData(AbstractBaseUser):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserData')
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile_number"]
    
    def __str__(self):
        return str(self.mobile_number)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    profile_img = models.ImageField(blank=True)
    Bio = models.CharField(blank=True, max_length=200)
    medical_history = models.TextField(blank=True, null=True)
    is_professional = models.BooleanField(default=False, blank=True, null=True)
    location = models.CharField(blank=True, max_length=200, null=True)
    last_updated = models.DateTimeField(auto_now=True)  # Automatically updates when the record is saved
    date_of_birth = models.DateField(blank=True, null=True)  # DOB

    def __str__(self):
        return self.user.username
    
    
class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=now)
    logout_time = models.DateTimeField(null=True, blank=True)  # Store logout time
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} logged in at {self.login_time} and logged out at {self.logout_time or 'N/A'}"
    
class Customer(models.Model):
    CHOICE_TYPE = [
        ('home', 'Home'),
        ('office', 'Office'),
        ('other', 'Other')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)  # Changed to CharField
    address = models.CharField(max_length=255)
    address_type = models.CharField(max_length=10, choices=CHOICE_TYPE, default="home")
    custom_address_type = models.CharField(max_length=50, blank=True, null=True)  # Only used if "Other" is selected
    location = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)  # Changed to CharField
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    otp = models.CharField(max_length=5)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=5))

    def save(self, *args, **kwargs):
        # Set expiration time (e.g., 10 minutes from now)
        self.expires_at = timezone.now() + timezone.timedelta(minutes=10)
        super().save(*args, **kwargs)
        

# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(default=timezone.now)
    shipping_address = models.TextField()
    tracking_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['order_date']),
        ]

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

    def clean(self):
        """
        Ensure the total_price matches the sum of all OrderItems.
        """
        calculated_price = sum(
            item.total_price for item in self.items.all()  # Use related_name='items' in OrderItem
        )
        if self.total_price != calculated_price:
            raise ValidationError("Total price does not match the sum of OrderItem prices.")

    def save(self, *args, **kwargs):
        """
        Automatically clean the model before saving.
        """
        self.clean()
        super().save(*args, **kwargs)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} for {self.user.username}'
    
class Coupon(models.Model):
    # Available types of discounts
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed'),
    ]
    
    # Basic Coupon Details
    brand = models.ForeignKey(Brand, related_name='coupon', on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(help_text="Description of the coupon.")
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # for percentage-based discounts
    min_cart_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    applicable_brands = models.TextField(null=True, blank=True)  # Brands that the coupon applies to (comma-separated)
    applicable_products = models.TextField(null=True, blank=True)  # Products the coupon applies to
    additional_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    terms_and_conditions = models.TextField()

    def __str__(self):
        return self.code

    def is_valid(self):
        # Check if the coupon is expired and meets the conditions
        if self.expiration_date and self.expiration_date < timezone.now():
            return False
        return True

    def get_discount(self, order_total):
        """
        Calculate the discount for an order based on the coupon type.
        """
        if self.discount_type == 'percentage':
            discount = order_total * (self.discount_value / 100)
            if self.max_discount:
                discount = min(discount, self.max_discount)
        elif self.discount_type == 'fixed':
            discount = self.discount_value
        else:
            discount = 0

        if self.additional_discount:
            discount += self.additional_discount

        return discount


# Order Item Model (for many-to-many relationship between Order and Product)
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, related_name='order_item', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} in order {self.order.id}'
    
    def apply_coupon(self):
        if self.coupon and self.coupon.is_valid():
            # Apply the discount based on coupon type
            if self.coupon.discount_type == 'percentage':
                discount = self.total_amount * (self.coupon.discount_value / 100)
                if self.coupon.max_discount:
                    discount = min(discount, self.coupon.max_discount)
                self.total_amount -= discount
            elif self.coupon.discount_type == 'fixed':
                self.total_amount -= self.coupon.discount_value
            return self.total_amount
        return self.total_amount
    
    
# Prescription Model
class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=200)
    prescription_file = models.FileField(upload_to='prescriptions/')
    issued_date = models.DateField()
    medicines = models.ManyToManyField(Product)

    def __str__(self):
        return f'Prescription for {self.user.username}'