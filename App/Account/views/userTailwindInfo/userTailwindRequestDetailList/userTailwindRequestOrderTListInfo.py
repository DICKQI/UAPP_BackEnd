from App.Tailwind.models import TailwindRequest
from Common.userAuthCommon import check_login, getUser
from Common.dictInfo import model_to_dict
from Common.paginator import paginator
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView


class UserTailwindRequestOrderTListView(APIView):

    @check_login
    def get(self, request):
        '''
        获得当前用户已被接单等待完成的订单
        :param request:
        :return:
        '''
        user = getUser(email=request.session.get("login"))
        page = request.GET.get('page')
        orderT_tailwind_request_list_obj = TailwindRequest.objects.filter(
            Q(initiator=user) &
            Q(status='orderT')
        )
        orderT_tailwind_request_list = paginator(orderT_tailwind_request_list_obj, page)

        orderT_tailwind_request = [model_to_dict(ott) for ott in orderT_tailwind_request_list]

        return JsonResponse({
            'status': True,
            'orderT_tailwind_request': orderT_tailwind_request,
            'has_next': orderT_tailwind_request_list.has_next(),
            'has_previous': orderT_tailwind_request_list.has_previous()
        })
