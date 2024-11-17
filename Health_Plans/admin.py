from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')  # Display name, slug, and created date
    search_fields = ('name',)  # Enable search by name
    ordering = ('name',)  # Order alphabetically by name


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'category', 'created_at')  # Display name, age, category, and created date
    list_filter = ('category',)  # Filter by category
    search_fields = ('name', 'description')  # Search by name and description
    ordering = ('-created_at',)  # Order by created date

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'created_at')  # Display question, category, and created date
    list_filter = ('category',)  # Filter by category
    search_fields = ('question', 'answer')  # Search by question and answer
    ordering = ('-created_at',)  # Order by created date



@admin.register(MedicalPartner)
class MedicalPartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'website', 'created_at')
    search_fields = ('name', 'email')
    ordering = ('name',)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'partner', 'price', 'duration', 'created_at')
    search_fields = ('plan_name', 'partner__name')
    ordering = ('-created_at',)



@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'phone_number', 'name', 'selected_at', 'is_active')
    list_filter = ('plan', 'is_active')
    search_fields = ('user__username', 'plan__plan_name')

    def phone_number(self, obj):
        # Fetch the phone number from the UserContact model
        contact = UserContact.objects.filter(user=obj.user).first()
        return contact.phone_number if contact else 'N/A'

    def name(self, obj):
        # Fetch the name from the UserContact model
        contact = UserContact.objects.filter(user=obj.user).first()
        return contact.name if contact else 'N/A'

    phone_number.short_description = 'Phone Number'
    name.short_description = 'Name'


@admin.register(UserContact)
class UserContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'phone_number', 'plan']
    search_fields = ['user__username', 'name', 'phone_number']
    list_filter = ['plan']
