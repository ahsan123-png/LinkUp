from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/chat/<str:receiver_username>/', PrivateChatConsumer.as_asgi()),
    path('ws/call/<str:receiver_username>/<str:call_type>/', CallConsumer.as_asgi()),
]
