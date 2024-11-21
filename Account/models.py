from django.db import models
from django.urls import reverse
import uuid
from django.utils import timezone
import random
import os
from django.utils.html import format_html
from django.utils.text import slugify
import string
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.timezone import now
# from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
from Products.models import Product

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

# Order Item Model (for many-to-many relationship between Order and Product)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} in order {self.order.id}'
    
    
# Prescription Model
class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=200)
    prescription_file = models.FileField(upload_to='prescriptions/')
    issued_date = models.DateField()
    medicines = models.ManyToManyField(Product)

    def __str__(self):
        return f'Prescription for {self.user.username}'