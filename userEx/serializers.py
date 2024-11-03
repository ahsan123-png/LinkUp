# serializers.py
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
# user serializer 
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=True)
    class Meta:
        model = UserEx
        fields = ['username', 'phone_number', 'email', 'password']
    def validate_username(self, value):
        if UserEx.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    def validate_email(self, value):
        if UserEx.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    def validate_phone_number(self, value):
        if UserEx.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        if not re.match(r'^\+\d{1,3}\d{9,15}$', value):  # Example regex for international phone number
            raise serializers.ValidationError("Invalid phone number format.")
        return value
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain both letters and numbers.")
        return value
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = UserEx.objects.create(**validated_data)
        return user
# ================ Login ================ 
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add extra user information to the response
        data.update({
            'user': {
                'username': self.user.username,
                'email': self.user.email
            }
        })
        return data
