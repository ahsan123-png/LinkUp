import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from userEx.models import PrivateMessage

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope['user']
        self.receiver_username = self.scope['url_route']['kwargs']['receiver_username']
        self.room_group_name = None
        try:
            self.receiver = await sync_to_async(User.objects.get)(username=self.receiver_username)
        except User.DoesNotExist:
            await self.close()
            return
        self.room_group_name = f'chat_{min(self.sender.id, self.receiver.id)}_{max(self.sender.id, self.receiver.id)}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        await sync_to_async(PrivateMessage.objects.create)(
            sender=self.sender,
            receiver=self.receiver,
            content=message
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.sender.username
            }
        )
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
