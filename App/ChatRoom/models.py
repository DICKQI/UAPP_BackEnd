from django.db import models
from django.utils.timezone import now
from App.Account.models import UserInfo
from django.db.models import Q


class ChatRoom(models.Model):
    """聊天室数据库模型"""
    chatRoomID = models.BigIntegerField(verbose_name='聊天室ID', primary_key=True, default=1, unique=True, blank=False)

    user1 = models.ForeignKey(UserInfo, verbose_name='用户1', on_delete=models.CASCADE, blank=False, default=None,
                              related_name='user1')

    user2 = models.ForeignKey(UserInfo, verbose_name='用户2', on_delete=models.CASCADE, blank=False, default=None,
                              related_name='user2')

    createTime = models.DateTimeField(verbose_name='创建时间', default=now, blank=False)

    is_cancel = models.BooleanField(verbose_name='是否注销', default=False, blank=False)

    chatLogCount = models.IntegerField(verbose_name='聊天记录计数器', default=0)

    class Meta:
        verbose_name = '聊天室'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'ChatRoom_ChatRoom'
        ordering = ['-createTime']

    def __str__(self):
        return str(self.chatRoomID)

    @classmethod
    def getUserChatRoomList(cls, user):
        return ChatRoom.objects.filter(
            Q(user1=user) |
            Q(user2=user)
        )


class ChatLog(models.Model):
    """聊天记录"""
    related_chat_room = models.ForeignKey(ChatRoom, verbose_name='关联聊天室', on_delete=models.CASCADE, default=None)

    speaker = models.ForeignKey(UserInfo, verbose_name='发言人', on_delete=models.CASCADE, default=None)

    speakTime = models.DateTimeField(verbose_name='发言时间', default=now, blank=False)

    content = models.TextField(verbose_name='内容', default=None, blank=False, max_length=300)

    class Meta:
        db_table = 'ChatRoom_ChatLog'

    def __str__(self):
        return self.speaker.nickname

    @classmethod
    def createAChatLog(cls, cid, user, content):
        newChatLog = ChatLog.objects.create(
            related_chat_room_id=cid,
            speaker=user,
            content=content
        )
        return newChatLog

    @classmethod
    def getChatRoomAllChatLog(cls, chatRoom):
        return ChatLog.objects.filter(related_chat_room=chatRoom)
