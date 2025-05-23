from django.urls import path
from .webhooks import stripe_webhook
from .views import fetch_balance, create_payment_intent, list_tickets

urlpatterns = [
    path('webhook/', stripe_webhook, name='stripe_webhook'),
    path('balance/', fetch_balance, name='fetch_balance'),
    path('create-payment-intent/<int:gig_id>/', create_payment_intent, name='create_payment_intent'),
    path('list-tickets/<int:gig_id>/', list_tickets, name='list_tickets'),
]