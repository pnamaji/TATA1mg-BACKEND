# #models
from django.db import models

# Create your models here.
class Category_s(models.Model):
    name = models.CharField(max_length=200)
    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    symptoms = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Test_s(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    

    
default_category_id = 1 
class Health_Packages(models.Model):
    category = models.ForeignKey(Category_s, related_name='packages', on_delete=models.CASCADE, default=default_category_id)
    name = models.CharField(max_length=200)
    safety_info = models.CharField(max_length=100, default="Safe")
    tests_included = models.ManyToManyField(Test_s, related_name='packages')
    num_tests = models.IntegerField()
    original_price = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    # description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name
    
# class TestDetail(models.Model):
#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('BOTH', 'Both'),
#     ]
    
#     # Reference to Health_Packages model for package selection
#     package = models.ForeignKey(Health_Packages, related_name='test_details', on_delete=models.CASCADE)
#     alternate_names = models.TextField(blank=True, null=True)  # Alternate names like "Fever panel"
#     sample_requirements = models.TextField(blank=True, null=True)  # Sample requirements like "Blood, Urine"
#     allowed_genders = models.TextField(blank=True, null=True)  # Sample requirements like "Blood, Urine"
#     preparation_instructions = models.TextField(blank=True, null=True)  # Test preparation instructions
   
#     def __str__(self):
#         return self.name




