from django.urls import path, include
from Products.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'api/categorytypewiseproducts', CategoryTypeProductView, basename='Category Type wise Products')
router.register(r'api/categorywiseproducts', CategoryProductView, basename='Category Wise Products')
router.register(r'api/spotlight', SpotlightProductViewSet, basename='Spotlight Product List')
router.register(r'api/healthconcerns', HealthConcernAPIView, basename='Health Concerns Categories List')
router.register(r'api/collagen', CollagenAPIView, basename='Collagen tag Products List')
router.register(r'api/personalcare', PersonalCareModelViewSet, basename='Personal Care tag Category List')
router.register(r'api/popularcategories', PopularCategoriesModelViewSet, basename='Popular Categories List')
router.register(r'brands', BrandViewSet)
router.register(r'address', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('categories/<int:category_id>/types/', TypeOfCategoryViewSet.as_view({'get': 'list'}), name='types-of-category-list'),
    # path('categories/<int:category_id>/types/<int:type_of_category_id>/products/', ProductViewSet.as_view({'get': 'list'}), name='products-list'),
    path('category/<int:category_id>/types/', TypeOfCategoryAPIView.as_view(), name='types_of_category'),
    path('category/type/<int:type_of_category_id>/products/', ProductAPIView.as_view(), name='products_by_type'),

    # Get SKU to all data of product
    path('api/products/<str:sku>/', ProductDetailAPIView.as_view(), name='Product Details API View'),

    # Coupon URL
    path('api/apply-coupon/', CouponApplyAPIView.as_view(), name='apply_coupon_api'),

    # Order Products
    path('api/create-order/', OrderCreateAPIView.as_view(), name='create_order_api'),
    
    # path('api/categorytypewiseproducts/', CategoryTypeProductView.as_view(), name='Category Type Wise Products'),

    # path('api/categorywiseproducts/', CategoryProductView.as_view(), name='Category Wise Products'),

    # path('api/spotlight/', SpotlightProductListAPIView.as_view(), name='spotlite-product-list'),

    # path('api/healthconcerns/', HealthConcernAPIView.as_view(), name='Health Concerns Category list'),

    # path('api/collagen/', CollagenAPIView.as_view(), name='Collagen Products list'),

    # path('api/personalcare/', PersonalCareAPIView.as_view(), name='Personal Care Categories list'),

    # path('api/popularcategories/', PopularCategoriesAPIView.as_view(), name='Popular Categories list'),

    path('api/<int:product_id>/upload-image/', ProductImageUploadView.as_view(), name='upload-product-image'),
]
if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)