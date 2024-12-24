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
        fields = "__all__"
        read_only_fields = ['id', 'username']
class UserRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=True)  # No additional validation
    username = serializers.CharField(required=False)

    class Meta:
        model = UserEx
        fields = ['username', 'email', 'phone_number', 'password', 'full_name']

    def validate_full_name(self, value):
        logger.debug(f"Validating full_name: {value}")
        name_parts = value.split(" ")
        if len(name_parts) == 1:
            self.context['first_name'] = name_parts[0]
            self.context['last_name'] = ''
        else:
            self.context['first_name'] = name_parts[0]
            self.context['last_name'] = " ".join(name_parts[1:])
        return value

    def create(self, validated_data):
        """
        Create a UserEx instance.
        """
        logger.debug(f"Creating user with data: {validated_data}")
        first_name = self.context.get('first_name', '')
        last_name = self.context.get('last_name', '')
        email = validated_data['email']
        username_base = email.split('@')[0]
        random_suffix = str(random.randint(1000, 9999))  # Random number
        unique_username = f"{username_base}{random_suffix}"
        while UserEx.objects.filter(username=unique_username).exists():
            random_suffix = str(random.randint(1000, 9999))
            unique_username = f"{username_base}{random_suffix}"
        user = UserEx.objects.create(
            username=unique_username,
            email=validated_data.get('email', ''),
            phone_number=validated_data['phone_number'],
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# # ================ Login ================ 
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         token['email'] = user.email
#         return token
#     def validate(self, attrs):
#         identifier = attrs.get('username') 
#         password = attrs.get('password')
#         try:
#             user = UserEx.objects.filter(email=identifier).first()
#             if not user:
#                 user = UserEx.objects.filter(phone_number=identifier).first()
#             if not user:
#                 raise ValidationError("User not found with this email/phone number")
#             if not user.check_password(password):
#                 raise ValidationError("Incorrect password")
#             data = super().validate(attrs)
#             data.update({
#                 'user': {
#                     'username': user.username,
#                     'email': user.email,
#                 }
#             })
#             return data
#         except UserEx.DoesNotExist:
#             raise ValidationError("User with given credentials not found")



class PrivateMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()

    class Meta:
        model = PrivateMessage
        fields = ['id', 'sender', 'receiver', 'content', 'media', 'sent_at']


