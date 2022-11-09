# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:pk/', consumers.ChatConsumer.as_asgi()),
]
