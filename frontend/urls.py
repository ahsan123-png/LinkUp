from .views import *
from django.urls import path , include

urlpatterns = [
    path('home/',home,name='home'),
    path('login/',loginUser,name='loginUser'),
    path('register/',register,name='register'),
    path('',register,name='register'),
    path('profile/',profile,name='profile'),
    path('logout_user/',user_logout,name='user_logout'),
    path('404/not_found/',notFound,name='notFound'),
]