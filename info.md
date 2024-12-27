# PrivateChatConsumer Code Explanation

This code defines a WebSocket consumer for handling private chat messages between users in a Django application using Channels. The `PrivateChatConsumer` class inherits from `AsyncWebsocketConsumer`, allowing it to handle asynchronous WebSocket connections.

## Imports

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from userEx.models import PrivateMessage

