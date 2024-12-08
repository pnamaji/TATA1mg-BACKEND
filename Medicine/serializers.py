from rest_framework import serializers
from .models import *

class MedicineSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'salt_composition', 'marketer', 'unit_type', 'description', 'storage', 'image', 'mrp', 'prescription_required', 'sku', 'created_at']

    def get_image(self, obj):
        if obj.image:  # Ensure the image exists
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url  # Fallback if no request context
        return None  # If no image is uploaded
    
class PrizeAndMedicineDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrizeAndMedicineDetail
        fields = ['id', 'medicine', 'mrp', 'discount_percentage', 'discounted_price', 'prescription_required', 'expiry_date', 'delivery_days', 'unit_type', 'description', 'views', 'created_at']
    
    def validate(self, data):
        """
        Custom validation for the fields if necessary.
        For example, you might want to ensure the `discounted_price` 
        is less than or equal to `mrp`.
        """
        if data.get('discounted_price') and data.get('mrp') and data['discounted_price'] > data['mrp']:
            raise serializers.ValidationError("Discounted price cannot be greater than MRP.")
        return data
    
class MedicineImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineImage
        fields = '__all__'


class OverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overview
        fields = '__all__'


class UseCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UseCase
        fields = '__all__'


class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = '__all__'


class SideEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SideEffect
        fields = '__all__'


class HowToUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowToUse
        fields = '__all__'


class HowDrugWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowDrugWork
        fields = '__all__'


class SafetyAdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyAdvice
        fields = '__all__'


class MissedDoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissedDose
        fields = '__all__'


class QuickTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickTip
        fields = '__all__'


class FactBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactBox
        fields = '__all__'


class PatientConcernSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientConcern
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class AuthorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorDetails
        fields = '__all__'