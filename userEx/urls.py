from .views import *
from django.urls import path , include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'friend-requests', FriendRequestViewSet, basename='friend-requests')
urlpatterns = [
    path('get/all/', UserExView.as_view(), name='user-list'),  # Get all users
    path('<int:user_id>/', UserExView.as_view(), name='user-detail'),
    path('search_user/', search_users, name='user-detail'),
    #====== users crediotionls ==================
    path('register/', UserRegistrationAPIView.as_view(),name="registerUser"),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('api/chat/history/<str:receiver_username>/', chat_history, name='chat_history'),
    path('api/chat/send/', send_private_message, name='send_private_message'),
    path('', include(router.urls))

]
# urls.py

