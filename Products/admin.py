from django.contrib import admin
from django import forms
from .models import *

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

# ==================== BRAND MODEL ====================
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# ==================== PRODUCT MODEL ====================
# class ProductAdminForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'
# 
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['categorytype'].queryset = TypesOfCategory.objects.none()

    #     if 'category' in self.data:
    #         try:
    #             category_id = int(self.data.get('category'))
    #             self.fields['categorytype'].queryset = TypesOfCategory.objects.filter(category_id=category_id)
    #         except (ValueError, TypeError):
    #             pass
    #     elif self.instance.pk:
    #         self.fields['categorytype'].queryset = TypesOfCategory.objects.filter(category=self.instance.category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_categories', 'get_types_of_category')  # Use custom methods for ManyToMany fields

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    get_categories.short_description = 'Categories'

    def get_types_of_category(self, obj):
        return ", ".join([type_of_category.name for type_of_category in obj.categorytype.all()])
    get_types_of_category.short_description = 'Types of Category'

@admin.register(TypesOfCategory)
class TypesOfCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_tags')  # Use custom method for ManyToMany fields

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

# ==================== PRODUCT IMAGE MODEL ====================
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product',)
    search_fields = ('product__name',)

# ==================== ORDER MODEL ====================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'order_date', 'shipping_address')
    search_fields = ('user__username', 'status')
    list_filter = ('status', 'order_date')
    date_hierarchy = 'order_date'
    readonly_fields = ('order_date',)

# ==================== ORDER ITEM MODEL ====================
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')

# ==================== REVIEW MODEL ====================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'review_date')
    search_fields = ('user__username', 'product__name')
    list_filter = ('rating', 'review_date')

# ==================== PRESCRIPTION MODEL ====================
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor_name', 'issued_date')
    search_fields = ('user__username', 'doctor_name')
    list_filter = ('issued_date',)
    date_hierarchy = 'issued_date'
    readonly_fields = ('issued_date',)
