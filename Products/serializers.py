from rest_framework import serializers
from .models import *

class MarketerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketer
        fields = ['id', 'name', 'address']
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'views']
      
class CategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)  # Products will be serialized for each category type
    tags = TagSerializer(many=True)  # assuming a ManyToMany relationship
    # img = serializers.ImageField(use_url=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'tags', 'description', 'img', 'views']

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
        fields = ['id', 'name', 'tags', 'category', 'description', 'img', 'views']

    def get_img_url(self, obj):
        request = self.context.get('request')
        if obj.img:  # Ensure the image is associated
            return request.build_absolute_uri(obj.img.url)
        return None  # Return None if no image exists
    
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

class BrandSerializer(serializers.ModelSerializer):
    # country_of_origin = CountrySerializer()
    # img = serializers.ImageField(use_url=True)
    tags = TagSerializer(many=True)  # assuming a ManyToMany relationship

    class Meta:
        model = Brand
        fields = ['id', 'name', 'category', 'address', 'description', 'img', 'tags']

    def get_img_url(self, obj):
        request = self.context.get('request')
        if obj.img:  # Ensure the image is associated
            return request.build_absolute_uri(obj.img.url)
        return None  # Return None if no image exists
    
class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  # assuming a ManyToMany relationship
    # brand = BrandSerializer(many=True)
    marketer = MarketerSerializer()
    category = CategorySerializer(many=True)
    categorytype = TypeOFCategorySerializer(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_type', 'quantity', 'stock', 'image',  'marketer', 'is_on_sale', 'sale_start_date', 'sale_end_date', 'selling_price', 'discounted_price', 'discount_percentage', 'views','average_rating', 'num_reviews', 'num_ratings', 'recent_reviews', 'review_summary', 'prescription_required', 'sku', 'expected_delivery_date', 'views','brand', 'tags', 'category', 'categorytype']

class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetails
        fields = ['id', 'description', 'key_ingredients', 'key_benefits', 'good_to_know', 'diet_type', 'help_with', 'allergen_information', 'product_form', 'net_quantity', 'direction_for_use', 'safety_information']

class ProductHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHighlight
        fields = ('id', 'description')


class ProductImageSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    # def get_image(self, obj):
    #     request = self.context.get('request')
    #     if request:
    #         return request.build_absolute_uri(obj.image.url)
    #     return f"{settings.MEDIA_URL}{obj.image.url}"

    # def get_image(self, obj):
    #     if obj.image:  # Ensure the image exists
    #         request = self.context.get('request')
    #         if request:
    #             return request.build_absolute_uri(obj.image.url)
    #         return obj.image.url  # Fallback if no request context
    #     return None  # If no image is uploaded

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

# class ReviewSerializer(serializers.ModelSerializer):
#     ratings_breakdown = serializers.SerializerMethodField()

#     class Meta:
#         model = Review
#         fields = ['id', 'user', 'product', 'rating', 'review_text', 'review_date', 'ratings_breakdown']

#     def get_ratings_breakdown(self, obj):
#         # Get all reviews for the product
#         reviews = Review.objects.filter(product=obj.product)

#         # Calculate total reviews
#         total_reviews = reviews.count()

#         # Count ratings for each star (1-5)
#         ratings_count = {star: reviews.filter(rating=star).count() for star in range(1, 6)}

#         # Calculate percentages
#         ratings_percentage = [
#             {"rating": star, "percentage": round((count / total_reviews) * 100, 2) if total_reviews > 0 else 0}
#             for star, count in ratings_count.items()
#         ]

#         return ratings_percentage

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'address']

class ProductInformationSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()  # Updated field name
    marketer = MarketerSerializer()

    class Meta:
        model = ProductInformation
        fields = ['id', 'product', 'cash_on_delivery', 'manufacturer', 'marketer', 'country_of_origin', 'expiry_date']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'review_text', 'review_date']

class ProductReviewSummarySerializer(serializers.Serializer):
    total_reviews_count = serializers.IntegerField()
    total_rating_count = serializers.IntegerField()
    average_rating = serializers.FloatField()  # Add the average rating field
    ratings_breakdown = serializers.ListField(child=serializers.DictField())
    reviews = ReviewSerializer(many=True)  # Include all reviews