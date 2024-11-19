from rest_framework import serializers
from .models import *
    
class ImageProductSerializer(serializers.ModelSerializer):
    # img_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['image']

    def get_image(self, obj):
        if obj.image:  # Ensure the image exists
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url  # Fallback if no request context
        return None  # If no image is uploaded
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
      
class CategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)  # Products will be serialized for each category type
    tags = TagSerializer(many=True)  # assuming a ManyToMany relationship
    # img = serializers.ImageField(use_url=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'tags', 'description', 'img']

    def get_img_url(self, obj):
        request = self.context.get('request')
        if obj.img:  # Ensure the image is associated
            return request.build_absolute_uri(obj.img.url)
        return None  # Return None if no image exists

class TypeOFCategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)  # Products will be serialized for each category type
    # img = serializers.ImageField(use_url=True)

    class Meta:
        model = TypesOfCategory
        fields = ['id', 'name', 'tags', 'category', 'description', 'img']

    def get_img_url(self, obj):
        request = self.context.get('request')
        if obj.img:  # Ensure the image is associated
            return request.build_absolute_uri(obj.img.url)
        return None  # Return None if no image exists

class BrandSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  # assuming a ManyToMany relationship

    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'img', 'tags']

    def get_img_url(self, obj):
        request = self.context.get('request')
        if obj.img:  # Ensure the image is associated
            return request.build_absolute_uri(obj.img.url)
        return None  # Return None if no image exists
    
class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  # assuming a ManyToMany relationship
    # brand = BrandSerializer(many=True)
    category = CategorySerializer(many=True)
    categorytype = TypeOFCategorySerializer(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity', 'image',  'description', 'selling_price', 'discounted_price', 'ad', 'discount_percentage', 'prescription_required', 'stock', 'sku', 'expiry_date', 'expected_delivery_date','brand', 'tags', 'category', 'categorytype']
  
class ProductHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHighlight
        fields = ('title', 'description')

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