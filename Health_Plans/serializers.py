# serializers.py
from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'created_at', 'updated_at']


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'name', 'age', 'description', 'category', 'created_at', 'updated_at']
        
    # Optional: Include category name in the serialized data
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'created_at', 'updated_at']
        
    # Optional: Include category name in the serialized data
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())



class MedicalPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalPartner
        fields = ['id', 'name', 'email', 'phone_number', 'address', 'logo', 'website', 'created_at', 'updated_at']


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'partner', 'plan_name', 'description', 'price', 'duration', 'benefits', 'image', 'created_at', 'updated_at']



class UserPlanSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='user.contact.phone_number', read_only=True)
    name = serializers.CharField(source='user.contact.name', read_only=True)
    plan_name = serializers.CharField(source='plan.plan_name', read_only=True)

    class Meta:
        model = UserPlan
        fields = ['user', 'plan_name', 'name', 'phone_number', 'selected_at', 'is_active']


class UserContactSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(), source='plan', write_only=True
    )

    class Meta:
        model = UserContact
        fields = ['user', 'name', 'phone_number', 'plan', 'plan_id']
        read_only_fields = ['user', 'phone_number']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().update(instance, validated_data)
# User = get_user_model()
# class UserPlanDetailSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username', read_only=True)
#     email = serializers.EmailField(source='user.email', read_only=True)

#     class Meta:
#         model = UserPlan
#         fields = ['username', 'email', 'plan', 'selected_at', 'is_active']