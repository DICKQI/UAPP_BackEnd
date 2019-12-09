from django.http import JsonResponse
from django.db.models import Q
from Common.userAuthCommon import getUser, check_login
from Common.dateInfo import generateFormatTime
from App.Account.models import UserInfo
from App.ChatRoom.models import ChatRoom
from rest_framework.views import APIView


def generateChatRoomID():
    time = generateFormatTime()
    oldChatRoom = ChatRoom.objects.first()
    if not oldChatRoom:
        newID = time + '0001'
        return int(newID)
    oldChatRoomTime = str(oldChatRoom.chatRoomID)[:len(str(oldChatRoom.chatRoomID)) - 4]
    if oldChatRoomTime == time:
        newID = str(int(str(oldChatRoom.chatRoomID)[-4:]) + 1)
    else:
        newID = '0001'
    for i in range(4 - len(newID)):
        newID = '0' + newID
    newID = time + newID
    return int(newID)


class ChatRoomInfoView(APIView):

    @check_login
    def get(self, request, uid):
        """
        发起与uid的聊天/创建于uid的聊天室
        :param request:
        :param uid: 对方账户的id
        :return: 返回聊天室id
        """
        to_user = UserInfo.objects.get(id=uid)
        myself = getUser(request.session.get('login'))
        chatRoom = ChatRoom.objects.filter(
            ((Q(user1=to_user) &
              Q(user2=myself)) |
             (Q(user1=myself) &
              Q(user2=to_user))) &
            Q(is_cancel=False)
        )  # 检查是否已经有该房间
        if chatRoom.exists():
            return JsonResponse({
                'status': True,
                'chat_room_id': chatRoom[0].chatRoomID
            })
        chatRoom = ChatRoom.objects.create(
            chatRoomID=generateChatRoomID(),
            user1=myself,
            user2=to_user
        )
        return JsonResponse({
            'status': False,
            'chat_room_id': chatRoom.chatRoomID
        })
