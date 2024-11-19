from django.contrib import admin
from .models import *

# Basic Admin Configurations
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Dr)
class DrAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bio')
    search_fields = ('name', 'bio')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Marketer)
class MarketerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'country_of_origin')
    search_fields = ('name', 'address')
    list_filter = ('country_of_origin',)


@admin.register(SaltComposition)
class SaltCompositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


# Medicine Model and Related Fields
class MedicineImageInline(admin.TabularInline):
    model = MedicineImage
    extra = 1


class OverviewInline(admin.StackedInline):
    model = Overview
    extra = 1


class UseCaseInline(admin.StackedInline):
    model = UseCase
    extra = 1


class HowToUseInline(admin.StackedInline):
    model = HowToUse
    extra = 1


class HowDrugWorksInline(admin.StackedInline):
    model = HowDrugWork
    extra = 1


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit_type', 'mrp', 'prescription_required', 'sku', 'created_at')
    search_fields = ('name', 'sku', 'description')
    list_filter = ('unit_type', 'prescription_required', 'created_at')
    inlines = [MedicineImageInline, OverviewInline, UseCaseInline, HowToUseInline, HowDrugWorksInline]


@admin.register(PrizeAndMedicineDetail)
class PrizeAndMedicineDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicine', 'mrp', 'discount_percentage', 'discounted_price', 'delivery_days', 'expiry_date')
    search_fields = ('medicine__name',)
    list_filter = ('unit_type', 'expiry_date')


@admin.register(MedicineImage)
class MedicineImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicine', 'image', 'created_at')
    search_fields = ('medicine__name',)


# Supplementary Models
@admin.register(Overview)
class OverviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicine', 'description')
    search_fields = ('medicine__name', 'description')


@admin.register(UseCase)
class UseCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicine', 'name')
    search_fields = ('medicine__name', 'name')


@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ('id', 'use_case', 'description')
    search_fields = ('use_case__name',)


@admin.register(SideEffect)
class SideEffectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


# Register the HowDrugWorks model
class HowDrugWorksAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'description')
    search_fields = ('medicine__name', 'description')

admin.site.register(HowDrugWork, HowDrugWorksAdmin)

# Register the SafetyAdvice model
class SafetyAdviceAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'alcohol', 'pregnancy', 'breast_feeding', 'driving', 'kidney', 'liver')
    search_fields = ('medicine__name', 'alcohol', 'pregnancy', 'breast_feeding', 'driving', 'kidney', 'liver')

admin.site.register(SafetyAdvice, SafetyAdviceAdmin)

# Optionally register the Medicine model if it's not already registered
# admin.site.register(Medicine)


@admin.register(MissedDose)
class MissedDoseAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicine', 'description')
    search_fields = ('medicine__name', 'description')


@admin.register(QuickTip)
class QuickTipAdmin(admin.ModelAdmin):
    list_display = ('id', 'tip_text')
    search_fields = ('tip_text',)


@admin.register(FactBox)
class FactBoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicine', 'chemmical_class', 'habit_forming', 'therapeutic_class', 'action_class')
    search_fields = ('medicine__name', 'chemmical_class')


@admin.register(PatientConcern)
class PatientConcernAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_resolved', 'resolved_by', 'views')
    search_fields = ('title', 'description')
    list_filter = ('is_resolved',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'question_type')
    search_fields = ('question_text',)
    list_filter = ('question_type',)


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'selected_option')
    search_fields = ('question__question_text', 'selected_option')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicine', 'question')
    search_fields = ('medicine__name', 'question')


@admin.register(AuthorDetails)
class AuthorDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'written_by', 'reviewed_by', 'created_at', 'updated_at')
    search_fields = ('written_by__name', 'reviewed_by__name')

