from App.Tailwind.models import TailwindRequest, TailwindTakeOrder
from Common.userAuthCommon import check_login, checkStudent
from Common.dictInfo import model_to_dict
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
import json


class RequestInfoView(APIView):
    INCLUDE_FIELDS = [
        'initiator', 'taskContent', 'beginTime', 'endTime', 'money', 'id', 'beginPlace', 'endPlace', 'serviceType'
    ]

    def post(self, request):
        """
        （地名）搜索订单
        :param request:
        :return:
        """
        jsonParams = json.loads((request.body).decode('utf-8'))
        place = jsonParams.get('place')
        result = TailwindRequest.objects.filter(
            Q(beginPlace__contains=place) |
            Q(endPlace__contains=place)
        )
        searchResult = [model_to_dict(re, fields=self.INCLUDE_FIELDS) for re in result if re.status == 'paid']
        return JsonResponse({
            'status': True,
            'count': result.count(),
            'searchResult': searchResult
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
