from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Gig, SeatRow
from custom_auth.models import Venue, ROLE_CHOICES
from rt_notifications.utils import create_notification
from django.forms.models import model_to_dict
from .serializers import GigSerializer, SeatRowSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_gigs(request):
    gigs = Gig.objects.all()
    return Response({'gigs': list(gigs.values())})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_gig(request, id):
    try:
        data = Gig.objects.get(id=id)

        serializer = GigSerializer(data)
        return Response({'gig': serializer.data})
    except Gig.DoesNotExist:
        return Response({'error': 'Gig not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_gig(request):
    user = request.user
    
    if user.role != ROLE_CHOICES.VENUE:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        venue = Venue.objects.select_related('user').get(user=user)
    except Venue.DoesNotExist:
        return Response({'error': 'Venue not found'}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    data['venue'] = {'id': venue.id}
    data['is_live'] = True
    
    serializer = GigSerializer(data=data)
    if serializer.is_valid():
        gig = serializer.save()
        create_notification(request.user, 'system', 'Gig created successfully', **gig.__dict__)
        return Response({
            'gig': serializer.data,
            'message': 'Gig created successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_gig_live_status(request, id):
    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        return Response({'error': 'Gig not found'}, status=status.HTTP_404_NOT_FOUND)
    
    is_live = request.data.get('is_live', None)

    if not isinstance(is_live, bool):
        return Response({'error': 'Invalid live status'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = GigSerializer(gig, data={'is_live': is_live})
    if serializer.is_valid():
        serializer.save()
        create_notification(request.user, 'system', 'Gig live status updated', **gig.__dict__)
        return Response({
            'gig': serializer.data,
            'message': 'Gig live status updated successfully'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_gig(request, id):
    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        return Response({'error': 'Gig not found'}, status=status.HTTP_404_NOT_FOUND)
    
    key = request.data.get('key', None)
    value = request.data.get('value', None)

    if not key or not value:
        return Response({'error': 'Invalid key or value'}, status=status.HTTP_400_BAD_REQUEST)

    allowed_keys = ['name', 'description', 'startDate', 'endDate', 'eventStartDate', 'eventEndDate', 'max_artist', 'flyer_text']
    if key not in allowed_keys:
        return Response({'error': 'Invalid key'}, status=status.HTTP_400_BAD_REQUEST)
    
    if key == 'is_live':
        return update_gig_live_status(request, id)

    serializer = GigSerializer(gig, data={key: value})
    if serializer.is_valid():
        serializer.save()
        create_notification(request.user, 'system', 'Gig updated successfully', **gig.__dict__)
        return Response({
            'gig': serializer.data,
            'message': 'Gig updated successfully'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_seat_row(request, gig_id):
    
    user = request.user
    if user.role != ROLE_CHOICES.VENUE:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
    try:
        venue = Venue.objects.select_related('user').get(user=user)
    except Venue.DoesNotExist:
        return Response({'error': 'Venue not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        gig = Gig.objects.get(id=gig_id, venue=venue)
    except Gig.DoesNotExist:
        return Response({'error': 'Gig not found'}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    data['gig'] = gig.id
    
    serializer = SeatRowSerializer(data=data)
    if serializer.is_valid():
        seat_row = serializer.save()
        create_notification(request.user, 'system', 'Seat row created successfully', **seat_row.__dict__)
        return Response({
            'seat_row': serializer.data,
            'message': 'Seat row created successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_gig_rows(request, gig_id):
    try:
        gig = Gig.objects.get(id=gig_id)
    except Gig.DoesNotExist:
        return Response({'error': 'Gig not found'}, status=status.HTTP_404_NOT_FOUND)
    
    seat_rows = SeatRow.objects.filter(gig=gig)
    return Response({'seat_rows': list(seat_rows.values())})
