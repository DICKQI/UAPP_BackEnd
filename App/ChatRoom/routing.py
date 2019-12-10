from django.urls import path
from .views import *

websocket_patterns = [
    path('ws/room/<int:rid>', ChatRoomBaseWebsocket),
]
