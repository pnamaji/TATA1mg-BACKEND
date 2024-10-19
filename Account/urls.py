from django.urls import path, include
from Account.views import *

urlpatterns = [
    path('api/signup/', SignUp.as_view(), name='SignUp'),
    path('api/signup/resend-otp/', ResendOTP.as_view(), name='resend-otp'),
    path('api/signup/verify-otp/', verify_otp_view.as_view(), name='verify-otp'),
    path('api/login/mobile-number/', LoginWithSMS.as_view(), name='login-sms'),
    path('api/login/mobile-number/verify-otp/', VerifyOTPForSMS.as_view(), name='login-sms-verify-otp'),
    path('api/login/email/', LoginWithEmail.as_view(), name='login-email'),
    path('api/login/email/verify-otp/', VerifyOTPForEmail.as_view(), name='login-email-verify-otp'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
