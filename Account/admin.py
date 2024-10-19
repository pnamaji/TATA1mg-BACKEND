from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import LoginHistory, UserData

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