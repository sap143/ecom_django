from django.urls import path
from .views import register_user, verify_otp, mfa_setup,login_with_mfa,logout_view, change_password_view,index

urlpatterns = [
    path('register/', register_user, name='register'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('mfa_setup/', mfa_setup, name='mfa_setup'),
    path('login/',login_with_mfa,name='login_with_mfa'),
    path('logout/',logout_view,name='logout_view'),
    path('change_password/',change_password_view,name='change_password_view'),
    path('',index,name='index')

    # Add any other URL patterns as needed
]


