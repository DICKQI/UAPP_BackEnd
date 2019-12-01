from App.Tailwind.models import TailwindRequest
from App.Account.models import UserConfig
from Common.dictInfo import model_to_dict
from Common.userAuthCommon import check_login, getUser, checkStudent
from Common.paginator import paginator

from django.http import JsonResponse
from rest_framework.views import APIView


def priority_list(requestOrder, request):
    """
    排序请求单列表，使之更符合目标用户
    版本号 1.0
    :return:
    """
    import json
    from time import localtime, time, strftime
    config = UserConfig.objects.get(relateUser=getUser(email=request.session.get('login')))
    # dormitory = config.dormitory  # 宿舍
    common_buildings = json.loads(config.commonAcademicBuilding)
    todayWeek = strftime('%a', localtime(time()))
    building_list = common_buildings[todayWeek]
    if len(building_list) == 0:
        return requestOrder
    else:
        for building in reversed(building_list):  # 使用倒序遍历，表示优先级
            # 将requestOrder里面的有beginPlace放前面
            for requests in requestOrder:
                if requests['beginPlace'] == building:
                    print(requests['requestID'])
                    tmp = requests
                    requestOrder.remove(requests)
                    requestOrder.insert(0, tmp)
        return requestOrder
    pass


class TailwindRequestListView(APIView):
    INCLUDE_FIELDS = [
        'initiator', 'taskContent', 'beginTime', 'endTime', 'money', 'requestID', 'beginPlace', 'endPlace',
        'serviceType', 'img'
    ]

    # @checkStudent
    # @check_login
    def get(self, request):
        '''
        获取发起单列表
        :param request:
        :return:
        '''
        try:
            page = request.GET.get('page')
            requestObj = TailwindRequest.objects.filter(status='paid')
            requestList = paginator(requestObj, page)

            requestOrder = [model_to_dict(re, fields=self.INCLUDE_FIELDS) for re in requestList]
            if request.session.get('login'):
                '''用户已登录，个性化设置'''
                requestOrder = priority_list(requestOrder, request)

            return JsonResponse({
                'status': True,
                'TailwindRequest': requestOrder,
                'has_previous': requestList.has_previous(),
                'has_next': requestList.has_next()
            })

        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': str(ex)
            }, status=403)
