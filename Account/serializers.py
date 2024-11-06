from rest_framework import serializers
from Account.models import *

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['email', 'mobile_number', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='user.username', read_only=True)  # User model से username को जोड़ें
    is_owner = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['is_owner', 'user', 'profile_img', 'location', 'last_updated', 'created_at']
        
    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.user == request.user  # True if the logged-in user is the owner
    
class ImageProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ['image']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:  # Ensure the image is associated
            return request.build_absolute_uri(obj.image.url)
        return None  # Return None if no thumbnail exists
    
class ProductSerializer(serializers.ModelSerializer):
    images = ImageProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['category', 'categorytype', 'images',  'name', 'brand', 'description', 'selling_price', 'discounted_price', 'ad', 'discount_percentage', 'prescription_required', 'stock', 'sku', 'expiry_date', 'expected_delivery_date']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'img']

class TypeOFCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TypesOfCategory
        fields = ['id', 'name', 'category', 'description', 'img']

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'img']