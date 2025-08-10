# serializers.py
import re
import random
from .models import *
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import logging
import pprint
logger = logging.getLogger(__name__)
# =========== Serializer ================
class UserExSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEx
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'full_name', 'profile_image', 'is_verified', 'status', 'date_joined'
        ]
        read_only_fields = ['id', 'username']
class UserRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    username = serializers.CharField(required=False)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = UserEx
        fields = ['username', 'email', 'password', 'full_name', 'profile_image']

    def validate_full_name(self, value):
        name_parts = value.split(" ")
        self.context['first_name'] = name_parts[0]
        self.context['last_name'] = " ".join(name_parts[1:]) if len(name_parts) > 1 else ''
        return value

    def create(self, validated_data):
        first_name = self.context.get('first_name', '')
        last_name = self.context.get('last_name', '')
        full_name = f"{first_name} {last_name}".strip()
        email = validated_data.get('email', '')
        username_base = email.split('@')[0] if email else 'user'
        unique_username = f"{username_base}{random.randint(1000, 9999)}"

        # Ensure uniqueness of username
        while UserEx.objects.filter(username=unique_username).exists():
            unique_username = f"{username_base}{random.randint(1000, 9999)}"

        # Handle default image if not provided
        profile_image = validated_data.get('profile_image', 'profile_images/defulat-image.jpg')

        user = UserEx.objects.create(
            username=unique_username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            profile_image=profile_image
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class PrivateMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()

    class Meta:
        model = PrivateMessage
        fields = ['id', 'sender', 'receiver', 'content', 'media', 'sent_at']


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user_name = serializers.CharField(source='from_user.full_name', read_only=True)
    to_user_name = serializers.CharField(source='to_user.full_name', read_only=True)
    profile_image = serializers.ImageField(source='from_user.profile_image', read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'from_user_name', 'to_user_name', 'profile_image', 'request_status', 'created_at']
