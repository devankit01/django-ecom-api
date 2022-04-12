from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<pk>/', ProductDetail.as_view()),

    path('category/', CategoryList.as_view()),
    path('category/<pk>/', CategoryDetail.as_view()),
    path('cart/', CartView.as_view()),
    path('cart-items/', CartItemListView.as_view()),
    path('cart-items/<pk>/', CartItemDetailView.as_view()),

    path('orders/', OrderView.as_view()),


    path('register/', RegisterView.as_view()),
    path('login/', LoginAPI.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-otp/', EmailOTPVerifyView.as_view(), name='verify_otp'),
    path('check_sqs/', check_Sqs, name="sqs"),
]
