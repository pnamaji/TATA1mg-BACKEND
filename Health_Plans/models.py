from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings
from Account.models import *




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., Diabetes, Mental Wellness
    image = models.URLField(max_length=200, blank=True, null=True)  # URL field for the image
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # SEO-friendly URL field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # parent = models.ForeignKey(
    #     'self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE
    # )  # For hierarchical categories

    class Meta:
        ordering = ['name']  # Orders categories alphabetically by default

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Auto-generates slug from name if not provided
        super(Category, self).save(*args, **kwargs)


class Experience(models.Model):
    name = models.CharField(max_length=100)  # Person's name
    age = models.PositiveIntegerField()  # Person's age
    description = models.TextField()  # Description of their experience
    category = models.ForeignKey(
        'Category', related_name='experiences', on_delete=models.CASCADE
    )  # Foreign Key to Category, making it compulsory


    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when experience was added
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for last update

    def __str__(self):
        return f"{self.name} - Age {self.age}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)  # FAQ question
    answer = models.TextField()  # Answer to the question
    category = models.ForeignKey(
        'Category', related_name='faqs', on_delete=models.CASCADE
    )  # Foreign Key to Category, making it compulsory

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when FAQ was added
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for last update

    def __str__(self):
        return self.question
    


class MedicalPartner(models.Model):
    name = models.CharField(max_length=255)  # Name of the partner company
    email = models.EmailField(unique=True)   # Contact email
    phone_number = models.CharField(max_length=15)  # Contact phone number
    address = models.TextField()  # Address of the partner
    logo = models.ImageField(upload_to='partners/logos/', blank=True, null=True)  # Partner's logo
    website = models.URLField(blank=True, null=True)  # Website URL

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Plan(models.Model):
    partner = models.ForeignKey(MedicalPartner, on_delete=models.CASCADE, related_name='plans')
    plan_name = models.CharField(max_length=255)  # Name of the plan
    description = models.TextField()  # Description of the plan
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Plan price
    duration = models.PositiveIntegerField()  # Duration in days
    benefits = models.TextField()  # List of benefits (can be a comma-separated list)
    image = models.ImageField(upload_to='plans/images/', blank=True, null=True)  # Image for the plan

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.plan_name} by {self.partner.name}"
    
class UserPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_plans')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='selected_users')
    selected_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the plan was selected
    is_active = models.BooleanField(default=True)  # Whether the plan is currently active

    def __str__(self):
        return f"{self.user.username} selected {self.plan.plan_name}"


class UserContact(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contact'
    )
    name = models.CharField(max_length=100)  # User's name
    phone_number = models.CharField(max_length=15, unique=True)  # Phone number
    plan = models.ForeignKey(
        Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_contacts'
    )  # Selected plan
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.phone_number} - Plan: {self.plan.plan_name if self.plan else 'No Plan'}"

