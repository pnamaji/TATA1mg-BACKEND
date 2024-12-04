from rest_framework import serializers
from .models import *
from urllib.parse import urljoin


class MarketerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketer
        fields = ['id', 'name', 'address']
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'views']

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'title', 'description', 'img', 'link', 'start_date', 'end_date', 'is_active']

class BrandSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ['id', 'name', 'address', 'description', 'img', 'tags']

    def get_tags(self, obj):
        # Return only 'id' and 'name' for each brand
        return obj.tags.values('id', 'name')

class TypeOFCategorySerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    ad = serializers.SerializerMethodField()

    class Meta:
        model = TypesOfCategory
        fields = ['id', 'name', 'description', 'img', 'views', 'ad', 'brand', 'tags']

    def get_ad(self, obj):
        # Initialize 'ads' as an empty list
        ads = []

        # Check if the related 'ad' exists
        if obj.ad.exists():  # Ensures there are related ads before accessing
            ads = obj.ad.values('id', 'title', 'img', 'link')

        # Add absolute URLs to the 'img' field for all ads
        request = self.context.get('request')  # Get the request context
        if request:  # Ensure request exists
            for ad in ads:
                if ad.get('img'):  # Safely check if 'img' exists
                    ad['img'] = urljoin(request.build_absolute_uri(settings.MEDIA_URL), ad['img'])
        
        return ads  # Return the list of ads
        
    def get_brand(self, obj):
        # Return only 'id', 'name', and a properly formatted 'img' URL for each brand
        brands = obj.brand.values('id', 'name', 'img')
        request = self.context.get('request')
        for brand in brands:
            if brand['img']:  # Check if the image field exists
                brand['img'] = urljoin(request.build_absolute_uri(settings.MEDIA_URL), brand['img'])
        return brands
    
    def get_tags(self, obj):
        # Return only 'id' and 'name' for each brand
        return obj.tags.values('id', 'name')

class CategorySerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()  # Custom field logic for brands
    subcategory = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    ad = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'img', 'views', 'ad', 'tags', 'brand', 'subcategory']

    def get_ad(self, obj):
        # Initialize 'ads' as an empty list
        ads = []

        # Check if the related 'ad' exists
        if obj.ad.exists():  # Ensures there are related ads before accessing
            ads = obj.ad.values('id', 'title', 'img', 'link')

        # Add absolute URLs to the 'img' field for all ads
        request = self.context.get('request')  # Get the request context
        if request:  # Ensure request exists
            for ad in ads:
                if ad.get('img'):  # Safely check if 'img' exists
                    ad['img'] = urljoin(request.build_absolute_uri(settings.MEDIA_URL), ad['img'])
        
        return ads  # Return the list of ads

    def get_subcategory(self, obj):
        request = self.context.get('request')  # Get the request object from the context
        subcategories = obj.subcategory.values('id', 'name', 'img')
        for subcategory in subcategories:
            if 'img' in subcategory and subcategory['img']:
                subcategory['img'] = urljoin(request.build_absolute_uri(settings.MEDIA_URL), subcategory['img'])  # Generate full URL
        return subcategories
    
    def get_brand(self, obj):
        request = self.context.get('request')  # Get the request object from the context
        brands = obj.brand.values('id', 'name', 'img')
        for brand in brands:
            if 'img' in brand and brand['img']:
                brand['img'] = urljoin(request.build_absolute_uri(settings.MEDIA_URL), brand['img'])  # Generate full URL
        return brands
    
    def get_tags(self, obj):
        # Return only 'id' and 'name' for each brand
        return obj.tags.values('id', 'name')
    
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()  # assuming a ManyToMany relationship
    marketer = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    categorytype = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_type', 'quantity', 'stock', 'image',  'marketer', 'is_on_sale', 'sale_start_date', 'sale_end_date', 'selling_price', 'discounted_price', 'discount_percentage', 'views','average_rating', 'num_reviews', 'num_ratings', 'recent_reviews', 'review_summary', 'prescription_required', 'sku', 'expected_delivery_date', 'views','brand', 'tags', 'category', 'categorytype']

    def get_tags(self, obj):
        # Return only 'id' and 'name' for each brand
        return obj.tags.values('id', 'name')
    
    def get_marketer(self, obj):
        marketer = obj.marketer  # Single Marketer object
        if marketer:
            return {'id': marketer.id,'name': marketer.name}
        return None  # Return None if no marketer is associated
    
    def get_category(self, obj):
        # Return only 'id' and 'name' for each brand
        return obj.category.values('id', 'name')
    
    def get_categorytype(self, obj):
        # Return only 'id' and 'name' for each brand
        return obj.categorytype.values('id', 'name')

class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetails
        fields = ['id', 'description', 'key_ingredients', 'key_benefits', 'good_to_know', 'diet_type', 'help_with', 'allergen_information', 'product_form', 'net_quantity', 'direction_for_use', 'safety_information']

class ProductHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHighlight
        fields = ('id', 'description')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def validate(self, data):
        # Check if address_type is 'other' and custom_address_type is empty
        if data.get('address_type') == 'other' and not data.get('custom_address_type'):
            raise serializers.ValidationError({
                "custom_address_type": "This field is required when address type is 'Other'."
            })
        return data

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