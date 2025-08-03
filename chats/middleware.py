# chats/middleware.py

from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth import get_user_model
from jwt import decode as jwt_decode
from jwt.exceptions import InvalidTokenError
from channels.db import database_sync_to_async
from django.conf import settings

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):  # Inherit from BaseMiddleware
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")
        
        scope['user'] = AnonymousUser()

        if token:
            try:
                decoded_data = jwt_decode(token[0], settings.SECRET_KEY, algorithms=["HS256"])
                user = await self.get_user(decoded_data["user_id"])
                if user:
                    scope['user'] = user
            except InvalidTokenError:
                pass

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None