from App.Tailwind.models import TailwindRequest, TailwindTakeOrder
from App.Account.models import UserInfo
from django.http import JsonResponse
from django.db.models import Q
from django.utils.timezone import now
from Common.paginator import paginator
from Common.dictInfo import model_to_dict
from Common.userAuthCommon import check_login, getUser, checkStudent
from rest_framework.views import APIView
import json, datetime, oss2


class UserTailwindTakeOrderView(APIView):
    """用户对接受单的一系列操作"""

    @check_login
    # @checkStudent
    def get(self, request):
        """
        获取用户的所有接收单
        :param request:
        :return:
        """
        try:
            pass
        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': '错误信息：' + str(ex)
            }, status=403)

    @check_login
    # @checkStudent
    def put(self, request, rid):
        """
        用户接单
        :param request:
        :param rid:
        :return:
        """
        try:
            user = getUser(request.session.get('login'))
            tailwindRequest = getRequest(rid)
            if not request:
                return JsonResponse({
                    'status': False,
                    'errMsg': '请求单不存在'
                })
            newTakeOrder = TailwindTakeOrder.objects.create(
                takeID=generateNewTakeID(tailwindRequest.requestID),
                mandatory=user,
                tailwindRequest=tailwindRequest
            )
            # 修改request单的状态
            # tailwindRequest.status = 'orderT'
            return JsonResponse({
                'status': True,
                'newTakeID': newTakeOrder.takeID,
                # 'endTime': tailwindRequest.endTime
            })
        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': '错误信息：' + str(ex)
            }, status=403)


def getRequest(rid):
    request = TailwindRequest.objects.filter(
        Q(requestID=rid) &
        Q(status='paid')  # 一定要已支付且未被接单才能被接单
    )
    if not request.exists():
        return False
    return request[0]


def generateNewTakeID(requestID):
    """生成接受单id"""
    # oldTake = TailwindTakeOrder.objects.filter(takeID__gte=requestID)
    # print(oldTake[len(oldTake) - 1].takeID)
    # if not oldTake.exists():
    #     newID = int(str(requestID) + '001')
    # else:
    #     newID = str(int(str(oldTake[0].takeID)[16:18]) + 1)
    #     for i in range(3 - len(newID)):
    #         newID = '0' + newID
    #     newID = int(str(requestID) + newID)
    # return newID
