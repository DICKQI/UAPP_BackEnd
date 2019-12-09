from django.contrib import admin
from .models import ChatLog, ChatRoom


@admin.register(ChatRoom)
class AdminChatRoom(admin.ModelAdmin):
    list_per_page = 100
    list_display = ['chatRoomID', 'user1', 'user2', 'createTime', 'is_cancel']
