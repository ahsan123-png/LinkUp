from .views import *
from django.urls import path , include

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(),name="registerUser"),
    path('login/', LoginAPIView.as_view(), name='login'),
]
