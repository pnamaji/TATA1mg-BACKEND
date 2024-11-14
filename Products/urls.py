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
router.register(r'api/popularlabtestsproducts', PopularLabTestModelViewSet, basename='Popular Lab Test Products List')
router.register(r'api/supersavingdeals', SuperSavingDealsModelViewSet, basename='Super saving deals products list')
router.register(r'api/skincareproducts', SkinCareProductModelViewSet, basename='Skin Care Type of Category Products List')
router.register(r'api/combodealsproducts', ComboDealsProductsModelViewSet, basename='Combo Deals Tag Products List')
router.register(r'api/painrelief&coughandcold', PainReliefAndCoughAndColdModelViewSet, basename="Pain Relief & Cough and Cold Category Products")
router.register(r'brands', BrandViewSet)
router.register(r'address', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category/<int:category_id>/types/', TypeOfCategoryAPIView.as_view(), name='types_of_category'),
    path('category/type/<int:type_of_category_id>/products/', ProductAPIView.as_view(), name='products_by_type'),

    # Get SKU to all data of product
    path('api/products/<str:sku>/', ProductDetailAPIView.as_view(), name='Product Details API View'),

    # Coupon URL
    path('api/apply-coupon/', CouponApplyAPIView.as_view(), name='apply_coupon_api'),

    # Order Products
    path('api/create-order/', OrderCreateAPIView.as_view(), name='create_order_api'),

    path('api/<int:product_id>/upload-image/', ProductImageUploadView.as_view(), name='upload-product-image'),
]
if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)