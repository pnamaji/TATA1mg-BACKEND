#urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


# router = DefaultRouter()
# router.register(r'test-details', TestDetailViewSet)

urlpatterns = [
    # path('api/', include(router.urls)),

    # view categories
    path('categories/', CategoryListView.as_view(), name='category-list'),

    # view packages category-wise
    path('categories/<int:category_id>/packages/', PackageListView.as_view(), name='package-list'),

    # view package by id
    path('packages/<int:id>/', PackageDetailView.as_view(), name='package-detail'),

    # Add Categories
    path('api/categories/', CreateCategoryView.as_view(), name='create-category'),

    # Add Tests
    path('api/tests/', CreateTestView.as_view(), name='create-test'),

    # Add Health_Checkup Packages
    path('api/health-packages/', CreateHealthPackageView.as_view(), name='create-health-package'),





]
