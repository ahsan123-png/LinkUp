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
class UserRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=True)
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
    def generate_unique_username(self, first_name):
        while True:
            random_number = random.randint(1000, 9999) 
            username = f"{first_name.lower()}{random_number}"  
            if not User.objects.filter(username=username).exists(): 
                return username
    def validate_email(self, value):
        if UserEx.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    def validate_phone_number(self, value):
        if UserEx.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        if not re.match(r'^\+\d{1,3}\d{9,15}$', value):
            raise serializers.ValidationError("Invalid phone number format.")
        return value
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain both letters and numbers.")
        return value
    def create(self, validated_data):
        first_name = self.context.get('first_name') 
        last_name = self.context.get('last_name') 
        validated_data['first_name'] = first_name
        validated_data['last_name'] = last_name
        validated_data.pop('full_name', None)
        username = self.generate_unique_username(first_name)
        validated_data['username'] = username
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
        identifier = attrs.get('username') 
        password = attrs.get('password')
        try:
            user = UserEx.objects.filter(email=identifier).first()
            if not user:
                user = UserEx.objects.filter(phone_number=identifier).first()
            if not user:
                raise ValidationError("User not found with this email/phone number")
            if not user.check_password(password):
                raise ValidationError("Incorrect password")
            data = super().validate(attrs)
            data.update({
                'user': {
                    'username': user.username,
                    'email': user.email,
                }
            })
            return data
        except UserEx.DoesNotExist:
            raise ValidationError("User with given credentials not found")
