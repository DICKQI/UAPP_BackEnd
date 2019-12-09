from django.http import JsonResponse
from django.db.models import Q
from App.ChatRoom.models import ChatLog, ChatRoom
from rest_framework.views import APIView
from Common.userAuthCommon import check_login
from Common.dictInfo import model_to_dict


class ChatRoomChatLogView(APIView):

    @check_login
    def get(self, request, rid):
        """
        获取聊天室的内容
        :param request:
        :param rid:
        :return:
        """
        try:
            chatRoom = ChatRoom.objects.filter(chatRoomID=rid)
            if not chatRoom.exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '聊天室不存在'
                }, status=404)
            chatRoom = chatRoom[0]
            chat_room_chat_log = ChatLog.objects.filter(related_chat_room=chatRoom)
            log_result = [model_to_dict(cl) for cl in chat_room_chat_log]
            return JsonResponse({
                'status': True,
                'log': log_result
            })
        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': '错误信息：' + str(ex)
            }, status=403)

