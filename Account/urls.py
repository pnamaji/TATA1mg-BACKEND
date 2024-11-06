from django.urls import path, include
from Account.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/signin/send-otp/', LoginWithSMS.as_view(), name='SignUp'),
    path('api/signin/resend-otp/', ResendOTPForSMS.as_view(), name='resend-otp'),
    path('api/signin/verify-otp/', VerifyOTPForSMS.as_view(), name='verify-otp'),
    path('api/signin/', SignInView.as_view(), name='login-sms'),
    path('api/login/email/', LoginWithEmail.as_view(), name='login-email'),
    path('api/login/email/resend-otp/', ResendOTPForEmail.as_view(), name='login-sms-verify-otp'),
    path('api/login/email/verify-otp/', VerifyOTPForEmail.as_view(), name='login-email-verify-otp'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)