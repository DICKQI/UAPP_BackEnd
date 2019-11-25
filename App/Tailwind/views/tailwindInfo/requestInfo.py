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
