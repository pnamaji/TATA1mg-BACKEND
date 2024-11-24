from django.contrib import admin
from django import forms
from .models import *

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active', 'start_date', 'end_date')

# ==================== CUSTOMER MODEL ====================
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'city', 'zipcode', 'state')
    search_fields = ('full_name', 'phone_number', 'city', 'state')
    list_filter = ('city', 'state')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')       # Assuming the field name is 'name' instead of 'tag'
    search_fields = ('name',)           # Add a comma to make it a tuple
    list_filter = ('id', 'name')        # Ensure 'name' is the correct field


# ==================== COUPON MODEL ====================
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'is_percentage', 'valid_from', 'valid_to', 'used_count')
    list_filter = ('is_percentage', 'valid_from', 'valid_to')
    search_fields = ('code',)
    ordering = ('-valid_from',)
    readonly_fields = ('used_count',)

    def get_readonly_fields(self, request, obj=None):
        """Make 'code' field read-only after creation."""
        if obj:
            return self.readonly_fields + ('code',)
        return self.readonly_fields
# ==================== CATEGORY MODEL ====================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)

# ==================== TYPES OF CATEGORY MODEL ====================
# @admin.register(TypesOfCategory)
# class TypesOfCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'description')
#     search_fields = ('name', 'category__name')
#     list_filter = ('category',)

# ==================== COUNTRY MODEL ====================
# Customizing the admin view for the Country model
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Display ID and name fields
    search_fields = ('name',)  # Allow searching by country name
    list_filter = ('name',)  # Add a filter sidebar to filter by name

# Registering the model with the admin interface
admin.site.register(Country, CountryAdmin)

# ==================== BRAND MODEL ====================
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_categories', 'get_types_of_category','average_rating', 'num_ratings', 'num_reviews', 'image_preview')  # Use custom methods for ManyToMany fields

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    get_categories.short_description = 'Categories'

    def get_types_of_category(self, obj):
        return ", ".join([type_of_category.name for type_of_category in obj.categorytype.all()])
    get_types_of_category.short_description = 'Types of Category'

    def image_preview(self, obj):
        # Check if the product has an image and return the HTML tag
        if hasattr(obj, 'image') and obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

# Custom Admin for ProductHighlight
class ProductHighlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'Product', 'description', 'get_product_name')
    search_fields = ('Product__name', 'description')  # Allows searching by product name or description
    list_filter = ('Product',)  # Allows filtering by product
    ordering = ('Product',)  # Default ordering by Product

    def get_product_name(self, obj):
        return obj.Product.name  # Returns the name of the product for display
    get_product_name.short_description = 'Product Name'  # Customize the column title

    def __str__(self):
        return self.Product.name

# Registering the ProductHighlight model with its custom admin
admin.site.register(ProductHighlight, ProductHighlightAdmin)

@admin.register(TypesOfCategory)
class TypesOfCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_tags')  # Use custom method for ManyToMany fields

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

# ==================== PRODUCT PACKAGE SIZE MODEL ====================
@admin.register(PackageSize)
class PackageSize(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'selling_price', 'discount_percentage', 'discounted_price', 'stock')

# ==================== PRODUCT IMAGE MODEL ====================
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview')  # Use valid fields or methods

    def package_size(self, obj):
        return obj.product.quantity  # Access the 'quantity' field of the related PackageSize

    package_size.short_description = 'Package Size'

admin.site.register(ProductImage, ProductImageAdmin)

# ==================== REVIEW MODEL ====================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'review_date')
    search_fields = ('user__username', 'product__name')
    list_filter = ('rating', 'review_date')

class ProductInformationAdmin(admin.ModelAdmin):
    list_display = ('product', 'cash_on_delivery', 'manufacturer', 'marketer', 'country_of_origin', 'expiry_date')  # Fields to display in the list view
    list_filter = ('cash_on_delivery', 'manufacturer', 'marketer', 'country_of_origin')  # Filters to help admin users
    search_fields = ('product__name', 'manufacturer__name', 'marketer__name')  # Searchable fields
    list_editable = ('cash_on_delivery',)  # Fields that can be edited directly in the list view
    

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')  # Fields to display in the list view
    search_fields = ('name',)  # Allow search by name
    list_filter = ('name',)  # Filters based on the name
    ordering = ('name',)  # Default ordering

class MarketerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')  # Fields to display in the list view
    search_fields = ('name',)  # Allow search by name
    list_filter = ('name',)  # Filters based on the name
    ordering = ('name',)  # Default ordering

# Registering the models with the admin site
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Marketer, MarketerAdmin)
admin.site.register(ProductInformation, ProductInformationAdmin)

@admin.register(ProductDetails)
class ProductDetailsAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('product', 'description', 'product_form', 'net_quantity')
    
    # Fields to search in the admin
    search_fields = ('product__name',  # Assuming `Product` has a `name` field 
                     'description','key_ingredients','key_benefits',
                     )
    
    # Fields to filter in the admin list view
    list_filter = ('product_form', 'diet_type')
    
    # Group fields in the detail view
    fieldsets = (
        ('Basic Information', {
            'fields': ('product', 'description'),
        }),
        ('Ingredients and Benefits', {
            'fields': ('key_ingredients', 'key_benefits'),
        }),
        ('Additional Information', {
            'fields': ('good_to_know', 'diet_type', 'help_with', 'allergen_information', 'product_form', 'net_quantity'),
        }),
        ('Usage and Safety', {
            'fields': ('direction_for_use', 'safety_information'),
        }),
    )
    
    # Automatically populate some fields or clean them
    prepopulated_fields = {}  # If you want to auto-fill fields like `description`

    # Enable in-line editing for related models if needed
    # inlines = []  # Add related inlines if any

    # Add actions
    actions = ['mark_as_safe']

    def mark_as_safe(self, request, queryset):
        queryset.update(safety_information="Safe for use")
        self.message_user(request, "Selected products marked as safe.")
    mark_as_safe.short_description = "Mark selected products as safe"