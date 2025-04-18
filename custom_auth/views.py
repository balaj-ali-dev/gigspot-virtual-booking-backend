# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from .models import User, Artist, Venue, Fan, ROLE_CHOICES
from .serializers import UserCreateSerializer
from utils.email import send_templated_email
from django.utils import timezone
from rt_notifications.utils import create_notification

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    try:
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Create the base user
            user = serializer.save()
        
            # Handle role-specific profile creation
            role = serializer.validated_data.get('role', ROLE_CHOICES.FAN)
            
            if role == ROLE_CHOICES.ARTIST:
                Artist.objects.create(
                    user=user,
                )
            elif role == ROLE_CHOICES.VENUE:
                Venue.objects.create(
                    user=user,
                )
            elif role == ROLE_CHOICES.FAN:
                Fan.objects.create(
                    user=user,
                )
            
            return Response({
                'user': serializer.data,
                'message': f'{role.capitalize()} account created successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([AllowAny])
def verify_otp(request):
    try:
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.ver_code != otp:
            return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.email_verfied:
            return Response({"detail": "Email already verified"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.ver_code_expires < timezone.now():
            return Response({"detail": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.email_verfied = True
        user.ver_code = None
        user.ver_code_expires = None
        user.save()
        
        return Response({"detail": "Email verified successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def resend_otp(request, email):
    try:
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.email_verfied:
            return Response({"detail": "Email already verified"}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = user.gen_otp()
        send_templated_email('OTP Verification', [user.email], 'otp_verification', {'otp': otp})
        
        return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({"detail": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.email_verfied:
            return Response({"detail": "Email not verified"}, status=status.HTTP_400_BAD_REQUEST)
        
        login(request, user)
        create_notification(user, 'system', 'Recent Activity', description='You have successfully logged in.')
        return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        logout(request)  # No need to pass user explicitly
        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


