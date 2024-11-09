from django.urls import path, include
from Account.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'categories', CategoryViewSet, basename='category')
# router.register(r'brands', BrandViewSet)
# router.register(r'address', CustomerViewSet)

urlpatterns = [
    path('api/signin/send-otp/', LoginWithSMS.as_view(), name='SignUp'),
    path('api/signin/resend-otp/', ResendOTPForSMS.as_view(), name='resend-otp'),
    path('api/signin/verify-otp/', VerifyOTPForSMS.as_view(), name='verify-otp'),
    path('api/signin/', SignInView.as_view(), name='login-sms'),
    path('api/login/email/', LoginWithEmail.as_view(), name='login-email'),
    path('api/login/email/resend-otp/', ResendOTPForEmail.as_view(), name='login-sms-verify-otp'),
    path('api/login/email/verify-otp/', VerifyOTPForEmail.as_view(), name='login-email-verify-otp'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    # path('', include(router.urls)),
    # path('categories/<int:category_id>/types/', TypeOfCategoryViewSet.as_view({'get': 'list'}), name='types-of-category-list'),
    # path('categories/<int:category_id>/types/<int:type_of_category_id>/products/', ProductViewSet.as_view({'get': 'list'}), name='products-list'),

    # # Get SKU to all data of product
    # path('api/products/<str:sku>/', ProductDetailAPIView.as_view(), name='Product Details API View'),

    # # Coupon URL
    # path('api/apply-coupon/', CouponApplyAPIView.as_view(), name='apply_coupon_api'),

    # # Order Products
    # path('api/create-order/', OrderCreateAPIView.as_view(), name='create_order_api'),
]
if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)