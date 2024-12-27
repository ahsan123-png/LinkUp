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
# =================== Audio Video Call ================
class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.caller = self.scope['user']
        self.receiver_username = self.scope['url_route']['kwargs']['receiver_username']
        self.call_type = self.scope['url_route']['kwargs']['call_type']  # Either 'voice' or 'video'
        self.room_group_name = f'call_{self.caller.id}_{self.receiver_username}'

        try:
            self.receiver = await sync_to_async(User.objects.get)(username=self.receiver_username)
        except User.DoesNotExist:
            await self.close()
            return

        # Add the WebSocket connection to a group for this call
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Send a call invite to the receiver
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_invite',
                'caller': self.caller.username,
                'call_type': self.call_type,
            }
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the group when the connection closes
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'offer':
            # Handle the incoming offer (from caller to receiver)
            await self.handle_offer(data)

        elif data['type'] == 'answer':
            # Handle the answer to the offer (accept or reject)
            await self.handle_answer(data)

        elif data['type'] == 'candidate':
            # Handle ICE candidate exchange
            await self.handle_ice_candidate(data)

        elif data['type'] == 'end_call':
            # Handle ending the call
            await self.handle_end_call()

    async def handle_offer(self, data):
        # Handle the offer (call initiation) from the caller
        offer = data['offer']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'offer_received',
                'offer': offer,
            }
        )

    async def handle_answer(self, data):
        # Handle the answer (acceptance/rejection) from the receiver
        answer = data['answer']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'answer_received',
                'answer': answer,
            }
        )

    async def handle_ice_candidate(self, data):
        # Handle ICE candidates for establishing the WebRTC connection
        candidate = data['candidate']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'ice_candidate',
                'candidate': candidate,
            }
        )

    async def handle_end_call(self):
        # Notify both parties that the call has ended
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_ended',
            }
        )

    # When call invite is received by the receiver, send this to their WebSocket
    async def call_invite(self, event):
        await self.send(text_data=json.dumps({
            'type': 'call_invite',
            'caller': event['caller'],
            'call_type': event['call_type'],
        }))

    # When offer is received, send this to the other party
    async def offer_received(self, event):
        await self.send(text_data=json.dumps({
            'type': 'offer_received',
            'offer': event['offer'],
        }))

    # When the answer is received (accept/reject), send this to both parties
    async def answer_received(self, event):
        await self.send(text_data=json.dumps({
            'type': 'answer_received',
            'answer': event['answer'],
        }))

    # When ICE candidates are exchanged, send this to the other party
    async def ice_candidate(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ice_candidate',
            'candidate': event['candidate'],
        }))

    # When the call ends, notify both parties
    async def call_ended(self, event):
        await self.send(text_data=json.dumps({
            'type': 'call_ended',
        }))