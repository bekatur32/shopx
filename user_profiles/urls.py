from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view()),

    path('seller/register',SellerRegisterView.as_view(), name='seller-register'),
    # path('wholeseller/register',WholeSellerRegisterView.as_view(), name='wholeseller-register'),

    path('refresh-token/', TokenRefreshView.as_view()),
    path('send-code-to-email/', ForgetPasswordSendCodeView.as_view(), name='send_password_reset_code'),
    path('verify-register-code/', UserVerifyRegisterCode.as_view(), name='verify_register_code'),
    path('forget-password/reset/', ForgetPasswordView.as_view(), name='reset_password'),
    path('become-seller/', BecomeSellerView.as_view(), name='become_seller'),
    path('reset-password-profile/', UserResetPasswordView.as_view(), name='reset_password'),


    path('profiles/', ListProfileApi.as_view(), name='reset_password'),
    path('profile/<int:id>', DetailProfileApi.as_view(), name='reset_password'),
    path('profile/update/<int:id>', UpdateProfileApi.as_view(), name='reset_password'),

]