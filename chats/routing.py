from django.urls import path
from .consumers import PrivateChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:receiver_username>/', PrivateChatConsumer.as_asgi()),  # WebSocket URL pattern
]
