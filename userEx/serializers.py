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
    is_friend = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = UserEx
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'full_name', 'profile_image', 'is_verified', 'status', 'date_joined', 'is_friend'
        ]
        read_only_fields = ['id', 'username']
    def get_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image.url  # this returns /media/... without domain
        return None
    def get_is_friend(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated or request.user == obj:
            return "False"

        # Debug print
        print(f"Checking relationship between {request.user.username} and {obj.username}")

        # Check for accepted friendship
        is_accepted = FriendRequest.objects.filter(
            request_status="accepted"
        ).filter(
            models.Q(from_user=request.user, to_user=obj) |
            models.Q(from_user=obj, to_user=request.user)
        ).exists()

        if is_accepted:
            print(f"Users are friends")
            return "True"

        # Check for pending outgoing request (current user sent request)
        is_pending_outgoing = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=obj,
            request_status="pending"
        ).exists()

        if is_pending_outgoing:
            print(f"Pending outgoing request")
            return "Pending"

        # Check for pending incoming request (current user received request)
        is_pending_incoming = FriendRequest.objects.filter(
            from_user=obj,
            to_user=request.user,
            request_status="pending"
        ).exists()

        if is_pending_incoming:
            print(f"Pending incoming request")
            return "Received"

        print(f"No relationship")
        return "False"
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

    # <-- declare the field
    total_received = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = [
            'id', 'from_user', 'to_user',
            'from_user_name', 'to_user_name', 'profile_image',
            'request_status', 'created_at', 'total_received'
        ]

    def get_total_received(self, obj):
        # Safely get request from context
        request = self.context.get('request', None)
        if request and request.user and not request.user.is_anonymous:
            # Count only pending (change/remove filter if you want "all" received)
            return FriendRequest.objects.filter(
                to_user=request.user,
                request_status='pending'
            ).count()
        return 0
