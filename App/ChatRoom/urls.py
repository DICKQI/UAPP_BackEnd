from django.urls import path
from django.conf.urls import include
from .views import *

app_name = 'ChatRoom'

urlpatterns = [
    path('room/<int:uid>/', ChatRoomInfoView.as_view(), name='chat_room_info'),  # 创建与用户聊天的聊天室
    path('room/log/<int:rid>/', ChatRoomChatLogView.as_view(), name='chat_room_log_info')
]
