from channels.generic.websocket import AsyncWebsocketConsumer
from App.ChatRoom.models import ChatRoom, ChatLog
from App.Account.models import UserInfo
import json
import datetime


class ChatRoomBaseWebsocket(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = object
        self.chatRoom = object
        self.nickname = str
        self.room_name = str
        self.room_group_name = str

    async def connect(self):
        room_id = self.scope['url_route']['kwargs']['rid']
        chatRoom = ChatRoom.objects.filter(chatRoomID=room_id)
        uid = self.scope['cookies'].get('uid', '')
        if not chatRoom.exists() or uid == '':  # 房间不存在或者用户id不存在
            await self.close()  # 拒绝连接
        else:
            self.user = UserInfo.objects.get(id=self.scope['cookies'].get('uid', ''))  # 用户对象
            self.chatRoom = chatRoom[0]  # 聊天室对象
            self.nickname = self.user.nickname  # 发言人昵称
            # 加入房间
            self.room_name = str(room_id)  # 房间id为房间名
            self.room_group_name = 'chat_' + self.room_name  # 房间组名

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def close(self, code=None):
        print('连接错误')

    async def disconnect(self, code):
        # 离开房间
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as ex:
            print(str(ex))

    async def receive(self, text_data, bytes_data=None):
        message = text_data
        ChatLog.objects.create(
            related_chat_room_id=self.chatRoom.chatRoomID,
            speaker=self.user,
            content=message,
            speakTime=datetime.datetime.now()
        )
        self.chatRoom.chatLogCount += 1
        self.chatRoom.save()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        send_data = {
            'message': message,
            'nickname': self.nickname
        }
        # 发送消息到websocket
        await self.send(text_data=json.dumps(send_data))
