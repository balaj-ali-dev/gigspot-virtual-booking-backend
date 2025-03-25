from django.urls import path
from .views import signup_view, verify_otp, resend_otp

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('resend-otp/<str:email>/', resend_otp, name='resend_otp'),
]