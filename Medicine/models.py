from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from datetime import datetime, timedelta

import os


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
def file_upload_to_dr_profile(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{instance.product.name}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('dr_profile/', new_filename)
    
class Dr(models.Model):
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    image = models.FileField(upload_to=file_upload_to_dr_profile, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Marketer(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=255)
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='marketer')


class SaltComposition(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

def file_upload_to_medicine_home(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{instance.name}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('medicine_home/', new_filename)

class Medicine(models.Model):
    UNIT_TYPES = [
        ('vial', 'Vial'),
        ('prefilled_syringe', 'Prefilled Syringe'),
        ('strip', 'Strip'),
        ('box', 'Box'),
        ('bottle', 'Bottle'),
    ]
    name = models.CharField(max_length=100)
    salt_composition = models.ForeignKey(SaltComposition, on_delete=models.CASCADE)
    marketer = models.ForeignKey(Marketer, on_delete=models.CASCADE, related_name='medicine')
    unit_type = models.CharField(max_length=50, choices=UNIT_TYPES)
    description = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    image = models.FileField(upload_to=file_upload_to_medicine_home, blank=True, null=True)
    mrp = models.DecimalField(max_digits=7, decimal_places=2)
    prescription_required = models.BooleanField(default=False)
    sku = models.CharField(max_length=100, unique=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # views = models.IntegerField(default=0)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Generate SKU if it's not already set
        if not self.sku:
            self.sku = self.generate_unique_sku()

        super().save(*args, **kwargs)
    
    def generate_unique_sku(self):
        base_sku = slugify(self.name)
        unique_sku = base_sku
        num = 1
        
        # Check if SKU exists, if it does, keep adding numbers to make it unique
        while Medicine.objects.filter(sku=unique_sku).exists():
            unique_sku = f"{base_sku}-{random.randint(1000, 9999)}"
            num += 1
        
        return unique_sku
    
    def get_share_link(self):
        return f"/Medicine/{self.sku}"
    
class PrizeAndMedicineDetail(models.Model):
    UNIT_TYPES = [
        ('vial', 'Vial'),
        ('prefilled_syringe', 'Prefilled Syringe'),
        ('strip', 'Strip'),
        ('box', 'Box'),
        ('bottle', 'Bottle'),
    ]
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='prize_medicine_details')
    mrp = models.DecimalField(max_digits=7, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    prescription_required = models.BooleanField(default=False)
    expiry_date = models.DateField(blank=True, null=True)
    delivery_days = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    unit_type = models.CharField(max_length=50, choices=UNIT_TYPES)
    description = models.CharField(max_length=100)
    expiry_date = models.DateField(blank=True, null=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.unit_type
    
    def save(self, *args, **kwargs):        
        if self.mrp and self.discount_percentage:
            # Calculate the discounted price based on percentage
            self.discounted_price = self.mrp - (self.mrp * self.discount_percentage / 100)
        elif self.mrp and self.discounted_price:
            # Calculate the discount percentage based on price
            self.discount_percentage = ((self.mrp - self.discounted_price) / self.mrp) * 100
        super().save(*args, **kwargs)

    # Expected delivery data calculate Method
    def expected_delivery_date(self):
        today = datetime.now().date() # Get current date
        delivery_date = today + timedelta(days=self.delivery_days)
        return delivery_date
    
def file_upload_to_medicine_image(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{instance.product.name}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('medicine_image/', new_filename)
    
class MedicineImage(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='medicine_image')
    image = models.FileField(upload_to=file_upload_to_medicine_image, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.image

class Overview(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='overview')
    description = models.TextField()

    def __str__(self):
        return self.description
    
class UseCase(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='usecase')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

class Benefit(models.Model):
    use_case = models.ForeignKey(UseCase, on_delete=models.CASCADE)
    description = models.TextField()

class SideEffect(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name
    
class HowToUse(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='how_to_use')
    description = models.TextField()

    def __str__(self):
        return self.description
    
class HowDrugWorks(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='how_drug_works')
    alcohol = models.CharField(max_length=100)
    a_description = models.TextField()
    pregnancy = models.CharField(max_length=100)
    p_description = models.TextField()
    breast_feeding = models.CharField(max_length=100)
    b_description = models.TextField()
    driving = models.CharField(max_length=100)
    d_description = models.TextField()
    kidney = models.CharField(max_length=100)
    k_description = models.TextField()
    liver = models.CharField(max_length=100)
    l_description = models.TextField()

    def __str__(self):
        return self.alcohol
    
class MissedDose(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='missed_dose')
    description = models.TextField()

    def __str__(self):
        return self.description
    
class QuickTip(models.Model):
    tip_text = models.TextField()

    def __str__(self):
        return self.tip_text
    
class FactBox(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='factbox')
    chemmical_class = models.CharField(max_length=100)
    habit_forming = models.CharField(max_length=100)
    therapeutic_class = models.CharField(max_length=100)
    action_class = models.CharField(max_length=100)

    def __str__(self):
        return self.chemmical_class
    
class PatientConcern(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  # Optional, if you want to associate concerns with users
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # Optional fields for additional information
    answer = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)  # E.g., "Cancer", "General Health"
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(Dr, on_delete=models.SET_NULL, null=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    # medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='question')
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=50, default='MCQ')  # Set default to MCQ

    # Multiple-choice options
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255,blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    option_e = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.question_text
    
class SurveyResponse(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE) 

    selected_option = models.CharField(max_length=255)
  # Store the letter of the selected option (A, B, C, D)

    def __str__(self):
        return self.selected_option
    
class FAQ(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='faq')
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
    
class AuthorDetails(models.Model):
    written_by = models.ForeignKey(Dr, on_delete=models.CASCADE, related_name='author_written')
    reviewed_by = models.ForeignKey(Dr, on_delete=models.CASCADE, related_name='author_reviewed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)