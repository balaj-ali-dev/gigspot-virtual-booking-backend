from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from custom_auth.models import User, Artist, Venue, Fan
from custom_auth.models import ROLE_CHOICES
from .models import UserSettings
from rt_notifications.utils import create_notification

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    try:
        user = request.user
        if user.role == ROLE_CHOICES.ARTIST:
            artist = Artist.objects.filter(user=user).first()
            return Response({
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'artist': artist
            })
        elif user.role == ROLE_CHOICES.VENUE:
            venue = Venue.objects.filter(user=user).first()
            return Response({
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'venue': venue
            })
        elif user.role == ROLE_CHOICES.FAN:
            fan = Fan.objects.filter(user=user).first()
            return Response({
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'fan': fan
            })
        else:
            return Response({
                'id': user.id,
                'email': user.email,
                'role': user.role
            })
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile_image(request):
    try:
        user = request.user
        
        # Check if file is in request.FILES
        if 'profileImage' not in request.FILES:
            return Response({"detail": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['profileImage']
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        if image_file.content_type not in allowed_types:
            return Response({"detail": "Invalid image type. Only JPEG, PNG, and GIF are allowed."},
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Validate file size (e.g., 5MB limit)
        if image_file.size > 5 * 1024 * 1024:  # 5MB
            return Response({"detail": "Image file too large. Maximum size is 5MB."},
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Save the image
        user.profileImage = image_file
        user.save()
        
        create_notification(user, 'system', 'Profile Image Updated', description='You have successfully updated your profile image.')
        return Response({
            "detail": "Profile image updated successfully",
            "image_url": user.profileImage.url if user.profileImage else None
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_notification_settings(request):
    try:
        user = request.user
        key = request.data.get('key')
        value = request.data.get('value')
        
        if not key or not value:
            return Response({"detail": "Key and value are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_settings = UserSettings.objects.filter(user=user).first()
        if not user_settings:
            user_settings = UserSettings.objects.create(user=user)
    
        allowed_keys = ['notify_by_email', 'notify_by_app'] 
        if key not in allowed_keys:
            return Response({"detail": "Invalid key"}, status=status.HTTP_400_BAD_REQUEST)
        
        if value not in [True, False]:
            return Response({"detail": "Value must be a boolean"}, status=status.HTTP_400_BAD_REQUEST)
        
        setattr(user_settings, key, value)
        user_settings.save()
        
        return Response({"detail": "Notification settings updated successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)