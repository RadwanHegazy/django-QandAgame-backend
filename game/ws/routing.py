from .consumers import RoomConsumer
from django.urls import path

ws_urlpatterns = [
    path('ws/room/<int:room_number>/', RoomConsumer.as_asgi())    
]