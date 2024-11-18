#serializers

from rest_framework import serializers
from .models import *


class TestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_s
        fields = ['id', 'name', 'description']

        
class HealthsPackageSerializer(serializers.ModelSerializer):
    tests_included = TestsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Health_Packages
        fields = [
            'id', 'name', 'safety_info', 'num_tests', 
            'original_price', 'discounted_price', 
            'discount_percent', 'tests_included'
        ]

class CategorysSerializer(serializers.ModelSerializer):
    packages = HealthsPackageSerializer(many=True, read_only=True)

    class Meta:
        model = Category_s
        fields = ['id', 'name', 'question', 'answer', 'symptoms', 'packages']


# # Serializer for TestDetail model
# class TestDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TestDetail
#         fields = ['id', 'package', 'alternate_names', 'sample_requirements',
#                     'allowed_genders', 'preparation_instructions']
    
