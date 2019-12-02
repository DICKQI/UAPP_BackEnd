from App.Tailwind.models import TailwindRequest, TailwindTakeOrder
from App.Account.models import UserInfo
from django.http import JsonResponse
from django.db.models import Q
from django.utils.timezone import now
from Common.paginator import paginator
from Common.dictInfo import model_to_dict
from Common.dateInfo import get_three_month_ago
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
            user = getUser(request.session.get('login'))
            ago = request.GET.get('ago')
            page = request.GET.get('page')
            three_month_ago = get_three_month_ago()
            if ago:
                tailwindTake = TailwindTakeOrder.objects.filter(
                    Q(mandatory=user)
                    & Q(create_time__lte=three_month_ago)  # 小于等于这个时间
                )
            else:
                tailwindTake = TailwindTakeOrder.objects.filter(
                    Q(mandatory=user)
                    & Q(create_time__gte=three_month_ago)  # 大于等于这个时间
                )
            takeList = paginator(tailwindTake, page)
            tailwindTakeOrder = [model_to_dict(tl, exclude='end_time') for tl in takeList]
            return JsonResponse({
                'status': True,
                'takeOrder': tailwindTakeOrder,
                'has_next': takeList.has_next(),
                'has_previous': takeList.has_previous()
            })
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
            if not tailwindRequest:
                return JsonResponse({
                    'status': False,
                    'errMsg': '请求单不存在或已经被接单啦'
                }, status=401)
            newTakeOrder = TailwindTakeOrder.objects.create(
                takeID=generateNewTakeID(tailwindRequest.requestID),
                mandatory=user,
                tailwindRequest=tailwindRequest
            )
            # 修改request单的状态
            tailwindRequest.status = 'orderT'
            tailwindRequest.save()
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
    id = int(str(requestID) + '001')
    while TailwindTakeOrder.objects.filter(takeID=id).exists():
        id += 1
    return id
