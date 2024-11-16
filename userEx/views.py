# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from .serializers import *
import logging
from rest_framework.views import APIView

from rest_framework.decorators import api_view
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
class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer