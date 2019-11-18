from App.Tailwind.models import TailwindRequest
from Common.dictInfo import model_to_dict
from Common.userAuthCommon import check_login, getUser, checkStudent
from Common.paginator import paginator

from django.http import JsonResponse
from rest_framework.views import APIView


class TailwindRequestListView(APIView):
    INCLUDE_FIELDS = [
        'initiator', 'taskContent', 'beginTime', 'endTime'
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
            requestObj = TailwindRequest.objects.all()
            requestList = paginator(requestObj, page)

            requestOrder = [model_to_dict(re, fields=self.INCLUDE_FIELDS) for re in requestList
                            if re.status == 'paid'
                            ]

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
