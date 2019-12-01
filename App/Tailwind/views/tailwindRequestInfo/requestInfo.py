from App.Tailwind.models import TailwindRequest, TailwindTakeOrder
from App.Account.models import UserInfo
from Common.userAuthCommon import check_login, checkStudent
from Common.dictInfo import model_to_dict
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
import json, datetime


class RequestInfoView(APIView):
    INCLUDE_FIELDS = [
        'initiator', 'taskContent', 'beginTime', 'endTime', 'money', 'requestID', 'beginPlace', 'endPlace',
        'serviceType'
    ]

    def post(self, request):
        """
        搜索发起单
        :param request:
        :return:
        """
        try:
            jsonParams = json.loads((request.body).decode('utf-8'))
            search_field = jsonParams.get('search_field')

            search_field = commonWordsTranslate(search_field)
            print(search_field)

            result = TailwindRequest.objects.filter(
                (Q(beginPlace__contains=search_field) |
                 Q(endPlace__contains=search_field))
                # & Q(beginTime__day=datetime.datetime.now())  # 只筛选今天的
            )
            searchResult = [model_to_dict(re, fields=self.INCLUDE_FIELDS) for re in result if re.status == 'paid']
            return JsonResponse({
                'status': True,
                # 'count': result.count,
                'searchResult': searchResult
            })
        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': '错误信息：' + str(ex)
            })

    @check_login
    # @checkStudent
    def get(self, request, tid):
        """
        获取请求单详情
        :param request:
        :param tid:
        :return:
        """
        try:
            tailwind_request = TailwindRequest.objects.filter(requestID=tid)
            if not tailwind_request.exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '请求单不存在'
                }, status=404)
            tailwind_request = tailwind_request[0]
            result = model_to_dict(tailwind_request)
            return JsonResponse({
                'status': True,
                'detail': result
            })
        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': '错误信息：' + str(ex)
            })


def commonWordsTranslate(search_fields):
    search_dict = open('config-data/search_field_dict.json', 'r')  # 加载字典
    search_dict = json.loads(search_dict.read())
    if search_dict.get(search_fields):
        return search_dict[search_fields]
    else:
        return search_fields

