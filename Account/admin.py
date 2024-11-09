from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from django import forms
# from .forms import ProductForm
# from .admin import TypesOfCategoryInline  # Ensure to import your inline class

class UserDataAdmin(BaseUserAdmin):
    list_display = ('mobile_number', 'email', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('mobile_number', 'email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {'fields': ('mobile_number', 'email', 'password1', 'password2')}),
    )
    search_fields = ('email', 'mobile_number')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(UserData, UserDataAdmin)

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'login_time', 'logout_time', 'ip_address']
    search_fields = ['user__username', 'ip_address']
    
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'Bio', 'is_professional', 'location', 'date_of_birth', 'last_updated')
    list_filter = ('location', 'date_of_birth')  # Ensure 'date_of_birth' is a model field
    search_fields = ('user__username', 'Bio', 'location')

    fieldsets = (
        (None, {
            'fields': ('user', 'Bio', 'location', 'is_professional','date_of_birth', 'profile_img')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('last_updated',),
        }),
    )
    readonly_fields = ('last_updated',)  # Ensure these fields exist in your model

# Register the UserProfile model with the admin site
admin.site.register(UserProfile, UserProfileAdmin)


# # Register Customer model
# @admin.register(Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'phone_number', 'city', 'zipcode', 'state')
#     search_fields = ('full_name', 'phone_number', 'city', 'state')
#     list_filter = ('city', 'state')

# # Register Category model
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     search_fields = ('name',)
#     list_filter = ('name',)

# # Register TypesOfCategory model
# @admin.register(TypesOfCategory)
# class TypesOfCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'description')
#     search_fields = ('name',)
#     list_filter = ('category',)

# # Register Brand model
# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     search_fields = ('name',)
    
# class ProductAdminForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Set initial queryset to none or filter by category if editing an existing instance
#         self.fields['categorytype'].queryset = TypesOfCategory.objects.none()

#         # Check if there's an instance or a selected category
#         if 'category' in self.data:
#             try:
#                 category_id = int(self.data.get('category'))
#                 self.fields['categorytype'].queryset = TypesOfCategory.objects.filter(category_id=category_id)
#             except (ValueError, TypeError):
#                 pass  # invalid input from the form data
#         elif self.instance.pk:  # Editing an existing instance
#             self.fields['categorytype'].queryset = self.instance.category.typesofcategory_set.all()

# class ProductAdmin(admin.ModelAdmin):
#     form = ProductAdminForm

#     class Media:
#         js = ('admin/js/category_type_filter.js',)  # Reference the custom JavaScript for AJAX filtering

# admin.site.register(Product, ProductAdmin)


# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ('product', 'image_preview')
#     search_fields = ('product__name',)
    
#     # Optional: Preview the image in the list display
#     def image_preview(self, obj):
#         if obj.image:
#             return f'<img src="{obj.image.url}" width="50" height="50" />'
#         return "No Image"
    
#     image_preview.allow_tags = True
#     image_preview.short_description = 'Image Preview'

# admin.site.register(ProductImage, ProductImageAdmin)

# # Register Order model
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'total_price', 'status', 'order_date', 'shipping_address', 'tracking_number')
#     search_fields = ('user__username', 'status', 'tracking_number')
#     list_filter = ('status', 'order_date')
#     date_hierarchy = 'order_date'

# # Register OrderItem model
# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'product', 'quantity', 'price')
#     search_fields = ('order__id', 'product__name')

# # Register Review model
# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('user', 'product', 'rating', 'review_date')
#     search_fields = ('user__username', 'product__name')
#     list_filter = ('rating', 'review_date')

# # Register Prescription model
# @admin.register(Prescription)
# class PrescriptionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'doctor_name', 'issued_date')
#     search_fields = ('user__username', 'doctor_name')
#     list_filter = ('issued_date',)
#     date_hierarchy = 'issued_date'