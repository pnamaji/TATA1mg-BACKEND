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

class CustomerSerializer(serializers.ModelSerializer):
    # Make user a read-only field
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Customer
        fields = '__all__'  # or specify fields like ['id', 'full_name', 'phone_number', 'address', 'city', 'state', 'zipcode']

    def validate(self, data):
        # Check if address_type is 'other' and custom_address_type is empty
        if data.get('address_type') == 'other' and not data.get('custom_address_type'):
            raise serializers.ValidationError({
                "custom_address_type": "This field is required when address type is 'Other'."
            })
        return data

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, source='orderitem_set', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'order_date', 'shipping_address', 'items']