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

# Create a logger instance
logger = logging.getLogger(__name__)
# user serializer 
class UserRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = UserEx
        # Include only the actual fields that exist on UserEx
        fields = ['username', 'email', 'phone_number', 'password', 'full_name']  # Do not include full_name in model fields

    def validate_full_name(self, value):
        # Split full name into first_name and last_name
        logger.debug(f"Validating full_name: {value}")
        name_parts = value.split(" ")

        if len(name_parts) == 1:
            # Single part name, treat as first_name and leave last_name as None
            self.context['first_name'] = name_parts[0]
            self.context['last_name'] = ''
        else:
            # Multiple part name, treat the first part as first_name and rest as last_name
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
        # Add first_name and last_name to validated_data from context
        first_name = self.context.get('first_name')  # Correct way to access first_name from context
        last_name = self.context.get('last_name')    # Correct way to access last_name from context

    # Ensure that first_name and last_name are in validated_data
        validated_data['first_name'] = first_name
        validated_data['last_name'] = last_name
        
        # Remove the 'full_name' field from validated data, as it's not part of the model
        validated_data.pop('full_name', None)
        username = self.generate_unique_username(first_name)
        validated_data['username'] = username
        # Hash the password
        validated_data['password'] = make_password(validated_data['password'])

        # Create and return the user
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
