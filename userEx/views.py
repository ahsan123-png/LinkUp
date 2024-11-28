# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from .serializers import *
import logging
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
logger = logging.getLogger(__name__)

class UserRegistrationAPIView(APIView):
    def post(self, request):
        # Create the serializer and pass the incoming request data
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            # If serializer is valid, create the user
            user = serializer.save()
            return Response({"message": "User registered successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ========== user Login ==============
class UserLoginAPIView(APIView):
    def post(self, request):
        username_or_email_or_phone = request.data.get('username_or_email_or_phone')
        password = request.data.get('password')
        if not username_or_email_or_phone or not password:
            return Response({'detail': 'Username or email or phone and password are required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            if '@' in username_or_email_or_phone:
                user = UserEx.objects.get(email=username_or_email_or_phone)
            else:
                user = UserEx.objects.get(phone_number=username_or_email_or_phone)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        except UserEx.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
# ============== get user by id =================
class UserExView(generics.GenericAPIView):
    queryset = UserEx.objects.all()  # Queryset for the UserEx model
    serializer_class = UserExSerializer
    def get(self, request, user_id=None):
        if user_id:
            # Get user by ID
            user = get_object_or_404(self.queryset, id=user_id)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            users = self.queryset.select_related().only('id', 'username', 'email', 'phone_number', 'is_verified')
            serializer = self.serializer_class(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        user = get_object_or_404(self.queryset, id=user_id)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = get_object_or_404(self.queryset, id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# getuser isinstance
def getUserEx(user):
    if isinstance(user, UserEx):
        return user
    else:
        try:
            return UserEx.objects.get(id=user.id)
        except UserEx.DoesNotExist:
            return None
    