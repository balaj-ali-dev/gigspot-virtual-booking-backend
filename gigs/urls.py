from django.urls import path
from .views import get_gigs, get_gig, create_gig, update_gig, update_gig_live_status

urlpatterns = [
    path('', get_gigs, name='get_gigs'),
    path('<int:id>/', get_gig, name='get_gig'),
    path('create/', create_gig, name='create_gig'),
    path('update/<int:id>/', update_gig, name='update_gig'),
    path('update-live-status/<int:id>/', update_gig_live_status, name='update_gig_live_status')
]