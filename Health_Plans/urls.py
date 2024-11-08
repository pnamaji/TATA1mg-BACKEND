from django.urls import path
from .views import *

urlpatterns = [
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    # Experience URLs
    path('experiences/', ExperienceListCreateView.as_view(), name='experience-list-create'),
    path('experiences/<int:pk>/', ExperienceDetailView.as_view(), name='experience-detail'),

    # FAQ URLs
    path('faqs/', FAQListCreateView.as_view(), name='faq-list-create'),
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),

    # Contact URLs
    path('user/contact/', UserContactView.as_view(), name='user_contact'),
    # Companies Medical Plans URLs 
    path('partners/', MedicalPartnerView.as_view(), name='medical-partners'),
    path('plans/', PlanView.as_view(), name='plans'),
    path('plans/<int:pk>/', PlanDetailView.as_view(), name='plan-detail'),

    # User Selected Plans URLs
    path('api/select-plan/<int:plan_id>/', SelectPlanAPIView.as_view(), name='select_plan'),

    # # Company can view which user selected plan
    path('api/user-plans/', UserPlanListView.as_view(), name='user_plan_list'),
    path('api/user-plans/<int:plan_id>/', UserPlanListView.as_view(), name='user_plan_detail'),



]
