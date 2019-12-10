from channels.generic.websocket import AsyncWebsocketConsumer
from App.Tailwind.models import TakeOrderUserRealtimeLocation, TailwindTakeOrder
from App.Account.models import UserInfo
import json
import datetime


class UserTailwindTakeOrderRealTimeWebsocketInfoView(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mandatory = object
        self.takeOrder = object
        self.userRealTimeLocation = object
        self.nickname = str
        self.room_name = str
        self.room_group_name = str

    async def connect(self):
        tid = self.scope['url_route']['kwargs']['tid']  # 获取url里面的take order id
        self.takeOrder = TailwindTakeOrder.objects.filter(takeID=tid)  # 获取接收单对象
        uid = self.scope['cookies'].get('uid', '')  # 获得cookie中的uid
        if not self.takeOrder.exists() or uid == '':
            """
            接收单不存在 || 用户未登录
            reject websocket
            """
            await self.close()
        else:
            self.takeOrder = self.takeOrder[0]
            self.mandatory = self.takeOrder.mandatory
            cookie_user = UserInfo.objects.get(id=uid)
            if self.mandatory != cookie_user or self.takeOrder.tailwindRequest.initiator != cookie_user:
                """用户权限检查"""
                await self.close()
            else:
                self.nickname = self.mandatory.nickname
                self.userRealTimeLocation = TakeOrderUserRealtimeLocation.objects.get(relateTakeOrder=self.takeOrder)
                self.room_name = str(tid)
                self.room_group_name = 'chat_' + self.room_name
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.accept()

    async def close(self, code=None):
        print('连接失败')

    async def disconnect(self, code):
        try:
            await self.channel_name.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as ex:
            print(str(ex))

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        self.userRealTimeLocation.latitude = message.get('latitude', '')
        self.userRealTimeLocation.longitude = message.get('longitude', '')
        self.userRealTimeLocation.speed = message.get('speed', '')
        self.userRealTimeLocation.save()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'location_message',
                'message': message
            }
        )

    async def location_message(self, event):
        """发送信息到websocket"""
        message = event['message']
        send_data = {
            'location': message,
            'tid': self.room_name,
            'mandatory': {
                'id': self.mandatory.id,
                'nickname': self.mandatory.nickname
            }
        }
        await self.send(text_data=json.dumps(send_data))
