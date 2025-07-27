import logging
from django.http import JsonResponse
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .serializers import PrivateMessageSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
#+++++++++++++++++++++++++++++++++++++++++++++++``
logger = logging.getLogger(__name__)
# ================== =====================
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer

class UserRegistrationAPIView(APIView):

    @extend_schema(
        request=UserRegistrationSerializer,  # This is what shows payload fields
        responses={201: UserRegistrationSerializer},
        description="Register a new user. A default profile image will be used if none is provided.",
        examples=[
            OpenApiExample(
                name="User Registration Example",
                value={
                    "full_name": "John Doe",
                    "email": "john@example.com",
                    "password": "securepassword123"
                    # You can optionally include "profile_image": "base64 or file" if needed
                },
                request_only=True
            )
        ],
        tags=["User Registration"]
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully",
                "user": serializer.data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
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
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful.",
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "full_name": f"{user.first_name} {user.last_name}",
                    },
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                }, status=status.HTTP_200_OK)
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
# ================== Private Chat =================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_private_message(request):
    """Send a private message to another user."""
    sender = request.user
    # sender = request.data.get('sender_username')
    receiver_username = request.data.get('receiver_username')
    content = request.data.get('content')
    if not receiver_username or not content:
        return Response({'error': 'receiver_username and content are required.'}, status=400)
    try:
        receiver = User.objects.get(username=receiver_username)
    except User.DoesNotExist:
        return Response({'error': 'Receiver not found.'}, status=404)
    private_message = PrivateMessage.objects.create(
        sender=sender,
        receiver=receiver,
        content=content
    )
    return Response({'message': 'Message sent successfully.', 'data': PrivateMessageSerializer(private_message).data})
# =================== Chat History =================
@login_required
def chat_history(request, receiver_username):
    sender = request.user
    receiver = User.objects.get(username=receiver_username)
    messages = PrivateMessage.objects.filter(
        sender=sender, receiver=receiver
    ) | PrivateMessage.objects.filter(
        sender=receiver, receiver=sender
    ).order_by('sent_at')
    message_list = [
        {
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "content": msg.content,
            "sent_at": msg.sent_at
        }
        for msg in messages
    ]
    return JsonResponse(message_list, safe=False)