from django.db import models
from django.db.models import Avg, Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
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
from django.contrib.auth.models import User
    
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
def file_upload_to_brand(instance, filename):
    return f'Brand/{filename}'
    
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    # category = models.ManyToManyField(Category, related_name='brand')
    # typeofcategory = models.ManyToManyField(TypesOfCategory, related_name='brand')
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='brands_tags')
    img = models.ImageField(upload_to=file_upload_to_brand, null=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name

def file_upload_to_category(instance, filename):
    return f'Category/{filename}'


    
def file_upload_to_categorytype(instance, filename):
    return f'TypeOfCategory/{filename}'
    
class TypesOfCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # category = models.CharField(Category, related_name='types_of_category')
    brand = models.ManyToManyField(Brand, related_name='types_of_category')
    tags = models.ManyToManyField(Tag, related_name='types_of_category')
    description = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to=file_upload_to_categorytype, blank=True, null=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='categories')
    img = models.ImageField(upload_to=file_upload_to_category, blank=True, null=True)
    views = models.IntegerField(default=0)
    subcategory = models.ManyToManyField(TypesOfCategory, related_name='category')
    brand = models.ManyToManyField(Brand, related_name='category')

    def __str__(self):
        return self.name
    

class Ad(models.Model):
    title = models.CharField(max_length=255)
    category = models.ManyToManyField(Category, related_name='ad')
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

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class Marketer(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name
    
def file_upload_to_products(instance, filename):
    ext = filename.split('.')[-1]
    product_name = slugify(instance.product.name)  # Ensure valid file names
    new_filename = f"{product_name}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('product_images/', new_filename)
    

# Product Model linked to Category
class Product(models.Model):
    UNIT_TYPES = [
        ('jar', 'Jar'),
        ('tube', 'Tube'),
        ('strip', 'Strip'),
        ('combo_pack', 'Combo Pack'),
        ('pump_bottle', 'Pump Bottle'),
        ('packet', 'Packet'),
        ('sachet', 'Sachet'),
        ('box', 'Box'),
        ('bottle', 'Bottle'),
    ]
    SELL_TYPES = [
        ('null', 'Null'),
        ('sell', 'Sell'),
        ('best_seller', 'Best Seller'),
    ]
    category = models.ManyToManyField(Category, related_name="products")  # Linking to Category model
    categorytype = models.ManyToManyField(TypesOfCategory, related_name="products")
    name = models.CharField(max_length=255)
    is_on_sale = models.CharField(default='null', choices=SELL_TYPES)
    sale_start_date = models.DateTimeField(null=True, blank=True)
    sale_end_date = models.DateTimeField(null=True, blank=True)
    unit_type = models.CharField(max_length=50, choices=UNIT_TYPES)
    quantity = models.CharField(max_length=255)
    stock = models.IntegerField(default=0, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
    tags = models.ManyToManyField(Tag, related_name='products')
    marketer = models.ForeignKey(Marketer, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    image = models.ImageField(upload_to=file_upload_to_products, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    prescription_required = models.BooleanField(null=True, blank=True, default=False)
    sku = models.CharField(max_length=255, unique=True, blank=True, editable=False)  # SKU field
    delivery_days = models.IntegerField(default=3)  # Admin se set hone wala field
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    # Review-related fields
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    num_ratings = models.IntegerField(default=0)
    num_reviews = models.IntegerField(default=0)
    recent_reviews = models.JSONField(default=list)
    review_summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    # def average_rating(self):
    #     reviews = self.reviews.all()
    #     if reviews.count() > 0:
    #         return round(sum(review.rating for review in reviews) / reviews.count(), 1)
    #     return 0
    
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
    description = models.TextField()

    def __str__(self):
        return self.description
       
class PackageSize(models.Model):
    UNIT_TYPES = [
        ('jar', 'Jar'),
        ('tube', 'Tube'),
        ('strip', 'Strip'),
        ('combo_pack', 'Combo Pack'),
        ('pump_bottle', 'Pump Bottle'),
        ('packet', 'Packet'),
        ('sachet', 'Sachet'),
        ('box', 'Box'),
        ('bottle', 'Bottle'),
    ]
    product = models.ForeignKey(Product, related_name='package_size', on_delete=models.CASCADE)
    unit_type = models.CharField(max_length=50, choices=UNIT_TYPES)
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

@receiver(post_save, sender=Product)
def create_package_size(sender, instance, created, **kwargs):
    if created:  # Only when a new Product is created
        PackageSize.objects.create(
            product=instance,  # Link to the Product instance
            quantity=instance.quantity,  # Use quantity from Product
            unit_type=instance.unit_type,  # Use unit_type from Product
            selling_price=instance.selling_price,
            discount_percentage=instance.discount_percentage,
            discounted_price=instance.discounted_price,
            stock=instance.stock,  # Default stock value
        )

class ProductImage(models.Model):
    package_size = models.ForeignKey(PackageSize, related_name='productImage', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to=file_upload_to_products)
    
    def __str__(self):
        return f"{self.product.name} Image"
    
    def image_preview(self):
        if self.image:
            return format_html('<img src="{}" width="50" height="50" />', self.image.url)
        return "No Image"
    
@receiver(post_save, sender=Product)
def create_product_image(sender, instance, created, **kwargs):
    if created:  # Only when a new Product is created
        ProductImage.objects.create(
            product=instance,  # Link to the Product instance
            image = instance.image, # Use image from Product
        )

class ProductDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_details')
    description = models.TextField()
    key_ingredients = models.TextField()
    key_benefits = models.TextField()
    good_to_know = models.TextField(blank=True, null=True)
    diet_type = models.TextField(blank=True, null=True)
    help_with = models.CharField(max_length=255, blank=True, null=True)
    allergen_information = models.TextField(blank=True, null=True)
    product_form = models.CharField(max_length=100, blank=True, null=True)
    net_quantity = models.CharField(max_length=100, blank=True, null=True)
    direction_for_use = models.TextField()
    safety_information = models.TextField()

    def __str__(self):
        return self.description

class ProductInformation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Add reference to Product
    cash_on_delivery = models.BooleanField(default=False)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True, blank=True)  # Manufacturer is optional
    marketer = models.ForeignKey(Marketer, on_delete=models.CASCADE)
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE)  # Will be populated from Brand
    expiry_date = models.DateField()  # Will be populated from Brand

    def __str__(self):
        return f"ProductInformation for {self.product.name if self.product else 'Unknown Product'}"

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

# Review Model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    review_text = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'
    

# ============================================Review update in product==============================================   
@receiver([post_save, post_delete], sender=Review)
def update_product_reviews(sender, instance, **kwargs):
    product = instance.product

    # Filter reviews with valid review text
    reviews_with_text = Review.objects.filter(product=product).exclude(review_text__isnull=True).exclude(review_text__exact='')
    all_reviews = Review.objects.filter(product=product)

    # Calculate average rating
    product.average_rating = round(all_reviews.aggregate(Avg('rating'))['rating__avg'] or 0, 1)

    # Update number of reviews (only counting those with review_text)
    product.num_reviews = reviews_with_text.count()

    # Update number of ratings (all reviews with a rating > 0)
    product.num_ratings = all_reviews.exclude(rating=0).count()

    # Get recent reviews (only those with review_text)
    recent_reviews_queryset = reviews_with_text.order_by('-review_date')[:5]
    product.recent_reviews = [
        {
            "user": review.user.username if review.user else "Anonymous",
            "rating": review.rating,
            "review_text": review.review_text,
        }
        for review in recent_reviews_queryset
    ]

    # Review summary
    product.review_summary = f"{product.num_reviews} reviews with an average rating of {product.average_rating}"

    # Save product updates
    product.save()