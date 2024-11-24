from .views import *
from django.urls import path , include

urlpatterns = [
    path('get/all/', UserExView.as_view(), name='user-list'),  # Get all users
    path('get/<int:user_id>/', UserExView.as_view(), name='user-detail'),
    #====== users crediotionls ==================
    path('register/', UserRegistrationAPIView.as_view(),name="registerUser"),
    path('login/', UserLoginAPIView.as_view(), name='login'),
]
