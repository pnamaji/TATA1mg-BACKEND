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
from datetime import datetime, timedelta, date
from django.conf import settings
from django.utils.timezone import now
from django.core.exceptions import ValidationError
# from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser

        
class Ad(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='ads/')
    link = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def is_active_now(self):
        return self.start_date <= date.today() <= self.end_date
    
    def save(self, *args, **kwargs):
        self.is_active = self.is_active_now()
        super().save(*args, **kwargs)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be earlier than start date.")
        super().clean()

    def __str__(self):
        return self.title

class Customer(models.Model):
    CHOICE_TYPE = [
        ('home', 'Home'),
        ('office', 'Office'),
        ('other', 'Other')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)  # Changed to CharField
    address = models.CharField(max_length=255)
    address_type = models.CharField(max_length=10, choices=CHOICE_TYPE, default="home")
    custom_address_type = models.CharField(max_length=50, blank=True, null=True)  # Only used if "Other" is selected
    locality = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)  # Changed to CharField
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name
    
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

def file_upload_to_category(instance, filename):
    return f'Category/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='categories')
    img = models.ImageField(upload_to=file_upload_to_category, blank=True, null=True)

    def __str__(self):
        return self.name
    
def file_upload_to_categorytype(instance, filename):
    return f'TypeOfCategory/{filename}'
    
class TypesOfCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ManyToManyField(Category, related_name='types_of_category')
    tags = models.ManyToManyField(Tag, related_name='types_of_category')
    description = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to=file_upload_to_categorytype, blank=True, null=True)

    def __str__(self):
        return self.name
    
def file_upload_to_brand(instance, filename):
    return f'Brand/{filename}'
    
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='brands_tags')
    img = models.ImageField(upload_to=file_upload_to_brand, null=True, blank=True)

    def __str__(self):
        return self.name
    
def file_upload_to_products(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{instance.product.name}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('product_images/', new_filename)
    

# Product Model linked to Category
class Product(models.Model):
    category = models.ManyToManyField(Category, related_name="products")  # Linking to Category model
    categorytype = models.ManyToManyField(TypesOfCategory, related_name="products")
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
    tags = models.ManyToManyField(Tag, related_name='products')
    description = models.TextField()
    image = models.ImageField(upload_to=file_upload_to_products, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    prescription_required = models.BooleanField(null=True, blank=True, default=False)
    sku = models.CharField(max_length=100, unique=True, blank=True, editable=False)  # SKU field
    expiry_date = models.DateField(blank=True, null=True)
    delivery_days = models.IntegerField(default=3)  # Admin se set hone wala field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    # Method to calculate discount percentage
    # def discount_percentage(self):
    #     if self.selling_price > 0:
    #         discount = ((self.selling_price - self.discounted_price) / self.selling_price) * 100
    #         return round(discount, 2)  # Returns discount percentage rounded to 2 decimal places
    #     return 0  # Return 0 if selling_price is not valid (e.g., zero or negative)
    
    def save(self, *args, **kwargs):
        # Generate SKU if it's not already set
        if not self.sku:
            self.sku = self.generate_unique_sku()  # Generate SKU based on instance attributes
        
        if self.selling_price and self.discount_percentage:
            # Calculate the discounted price based on percentage
            self.discounted_price = self.selling_price - (self.selling_price * self.discount_percentage / 100)
        elif self.selling_price and self.discounted_price:
            # Calculate the discount percentage based on price
            self.discount_percentage = ((self.selling_price - self.discounted_price) / self.selling_price) * 100
        super().save(*args, **kwargs)

    # Expected delivery data calculate Method
    def expected_delivery_date(self):
        today = datetime.now().date() # Get current date
        delivery_date = today + timedelta(days=self.delivery_days)
        return delivery_date
    
    def generate_unique_sku(self):
        base_sku = slugify(self.name)
        unique_sku = base_sku
        num = 1
        
        # Check if SKU exists, if it does, keep adding numbers to make it unique
        while Product.objects.filter(sku=unique_sku).exists():
            unique_sku = f"{base_sku}-{random.randint(1000, 9999)}"
            num += 1
        
        return unique_sku
    
    def get_share_link(self):
        return f"/Products/{self.sku}"
    
class ProductHighlight(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_highlight')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
       
class PackageSize(models.Model):
    product = models.ForeignKey(Product, related_name='package_size', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.quantity
    
    def save(self, *args, **kwargs):        
        if self.selling_price and self.discount_percentage:
            # Calculate the discounted price based on percentage
            self.discounted_price = self.selling_price - (self.selling_price * self.discount_percentage / 100)
        elif self.selling_price and self.discounted_price:
            # Calculate the discount percentage based on price
            self.discount_percentage = ((self.selling_price - self.discounted_price) / self.selling_price) * 100
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    package_size = models.ForeignKey(PackageSize, related_name='productImage', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=file_upload_to_products)
    
    def __str__(self):
        return f"Image for {self.package_size.name}"
    
    def image_preview(self):
        if self.image:
            return format_html('<img src="{}" width="50" height="50" />', self.image.url)
        return "No Image"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    is_percentage = models.BooleanField(default=False)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    used_count = models.IntegerField(default=0)

    def is_valid(self, total_price, cart_items, is_first_order):
        # Check validity conditions here
        return self.valid_from <= timezone.now() <= self.valid_to

    def apply_discount(self, total_price):
        if self.is_percentage:
            return total_price * (self.discount / 100)
        return self.discount

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
    
# Review Model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'
    
# Prescription Model
class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=200)
    prescription_file = models.FileField(upload_to='prescriptions/')
    issued_date = models.DateField()
    medicines = models.ManyToManyField(Product)

    def __str__(self):
        return f'Prescription for {self.user.username}'