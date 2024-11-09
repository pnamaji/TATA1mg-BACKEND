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
        
# class Customer(models.Model):
#     CHOICE_TYPE = [
#         ('home', 'Home'),
#         ('office', 'Office'),
#         ('other', 'Other')
#     ]
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
#     full_name = models.CharField(max_length=100)
#     phone_number = models.IntegerField()
#     address = models.CharField(max_length=255)
#     address_type = models.CharField(max_length=10, choices=CHOICE_TYPE, default="Home")
#     custom_address_type = models.CharField(max_length=50, blank=True, null=True)  # Only used if "Other" is selected
#     locality = models.CharField(max_length=255, blank=True, null=True)
#     city = models.CharField(max_length=100)
#     zipcode = models.IntegerField()
#     state = models.CharField(max_length=100)
    
#     def __str__(self):
#         return self.full_name

# def file_upload_to_category(instance, filename):
#     return f'Category/{filename}'

# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True, null=True)
#     img = models.FileField(upload_to=file_upload_to_category, blank=True, null=True)

#     def __str__(self):
#         return self.name
    
# def file_upload_to_categorytype(instance, filename):
#     return f'TypeOfCategory/{filename}'
    
# class TypesOfCategory(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     description = models.TextField(blank=True, null=True)
#     img = models.FileField(upload_to=file_upload_to_categorytype, blank=True, null=True)

#     def __str__(self):
#         return self.name
    
# def file_upload_to_brand(instance, filename):
#     return f'Brand/{filename}'
    
# class Brand(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True, null=True)
#     img = models.FileField(upload_to=file_upload_to_brand, null=True, blank=True)

#     def __str__(self):
#         return self.name
    
# def file_upload_to_products(instance, filename):
#     ext = filename.split('.')[-1]
#     new_filename = f"{instance.product.name}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
#     return os.path.join('product_images/', new_filename)
    

# # Product Model linked to Category
# class Product(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Linking to Category model
#     categorytype = models.ForeignKey(TypesOfCategory, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
#     description = models.TextField()
#     selling_price = models.DecimalField(max_digits=10, decimal_places=2)
#     ad = models.BooleanField(blank=True, null=True)
#     discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
#     discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     prescription_required = models.BooleanField(null=True, blank=True, default=False)
#     stock = models.IntegerField(default=0)
#     sku = models.CharField(max_length=100, unique=True, blank=True, editable=False)  # SKU field
#     expiry_date = models.DateField(blank=True, null=True)
#     delivery_days = models.IntegerField(default=3)  # Admin se set hone wala field
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
    
#     # Method to calculate discount percentage
#     # def discount_percentage(self):
#     #     if self.selling_price > 0:
#     #         discount = ((self.selling_price - self.discounted_price) / self.selling_price) * 100
#     #         return round(discount, 2)  # Returns discount percentage rounded to 2 decimal places
#     #     return 0  # Return 0 if selling_price is not valid (e.g., zero or negative)
    
#     def save(self, *args, **kwargs):
#         # Generate SKU if it's not already set
#         if not self.sku:
#             self.sku = self.generate_unique_sku()  # Generate SKU based on instance attributes
        
#         if self.selling_price and self.discount_percentage:
#             # Calculate the discounted price based on percentage
#             self.discounted_price = self.selling_price - (self.selling_price * self.discount_percentage / 100)
#         elif self.selling_price and self.discounted_price:
#             # Calculate the discount percentage based on price
#             self.discount_percentage = ((self.selling_price - self.discounted_price) / self.selling_price) * 100
#         super().save(*args, **kwargs)

#     # Expected delivery data calculate Method
#     def expected_delivery_date(self):
#         today = datetime.now().date() # Get current date
#         delivery_date = today + timedelta(days=self.delivery_days)
#         return delivery_date
    
#     def generate_unique_sku(self):
#         base_sku = slugify(self.name)
#         unique_sku = base_sku
#         num = 1
        
#         # Check if SKU exists, if it does, keep adding numbers to make it unique
#         while Product.objects.filter(sku=unique_sku).exists():
#             unique_sku = f"{base_sku}-{random.randint(1000, 9999)}"
#             num += 1
        
#         return unique_sku
    
#     def get_share_link(self):
#         return f"/Products/{self.sku}"

# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=file_upload_to_products)
    
#     def __str__(self):
#         return f"Image for {self.product.name}"
    
#     def image_preview(self):
#         if self.image:
#             return format_html('<img src="{}" width="50" height="50" />', self.image.url)
#         return "No Image"

# class Coupon(models.Model):
#     code = models.CharField(max_length=15, unique=True)
#     discount = models.DecimalField(max_digits=5, decimal_places=2)  # discount amount, e.g., 10 for 10%
#     is_percentage = models.BooleanField(default=True)  # True for % discount, False for fixed amount
#     valid_from = models.DateTimeField()
#     valid_to = models.DateTimeField()
#     usage_limit = models.PositiveIntegerField(null=True, blank=True)  # None for unlimited usage
#     used_count = models.PositiveIntegerField(default=0)
#     minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Minimum order for coupon
#     is_first_order_only = models.BooleanField(default=False)  # True if it's only for the first order
#     applicable_products = models.ManyToManyField(Product, blank=True)  # Set blank=True to allow coupons for all products

#     def is_valid(self, total_amount, cart_items, is_first_order):
#         # Check first-order condition
#         if self.first_order_only and not is_first_order:
#             return False

#         # Check minimum order amount
#         if total_amount < self.minimum_order_value:
#             return False

#         # Check applicable products
#         applicable = all(item['product_id'] in self.applicable_products.values_list('id', flat=True)
#                          for item in cart_items) if self.applicable_products.exists() else True
#         return applicable

#     def get_discount(self, total_amount):
#         return total_amount * (self.discount_percentage / 100)

# # Order Model
# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('confirmed', 'Confirmed'),
#         ('shipped', 'Shipped'),
#         ('delivered', 'Delivered'),
#         ('canceled', 'Canceled'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product, through='OrderItem')
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     order_date = models.DateTimeField(default=timezone.now)
#     shipping_address = models.TextField()
#     tracking_number = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return f'Order {self.id} by {self.user.username}'

# # Order Item Model (for many-to-many relationship between Order and Product)
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f'{self.product.name} in order {self.order.id}'
    
# # Review Model
# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     rating = models.PositiveSmallIntegerField()
#     review_text = models.TextField()
#     review_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Review by {self.user.username} for {self.product.name}'
    
# # Prescription Model
# class Prescription(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     doctor_name = models.CharField(max_length=200)
#     prescription_file = models.FileField(upload_to='prescriptions/')
#     issued_date = models.DateField()
#     medicines = models.ManyToManyField(Product)

#     def __str__(self):
#         return f'Prescription for {self.user.username}'