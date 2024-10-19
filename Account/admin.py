from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import LoginHistory, UserData, UserProfile

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
    list_display = ('user', 'full_name', 'Bio', 'location', 'date_of_birth', 'last_updated')
    list_filter = ('location', 'date_of_birth')  # Ensure 'date_of_birth' is a model field
    search_fields = ('user__username', 'full_name', 'Bio', 'location')

    fieldsets = (
        (None, {
            'fields': ('user', 'full_name', 'Bio', 'location', 'date_of_birth', 'profile_img', 'cover_img')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('last_updated',),
        }),
    )
    readonly_fields = ('last_updated',)  # Ensure these fields exist in your model

# Register the UserProfile model with the admin site
admin.site.register(UserProfile, UserProfileAdmin)