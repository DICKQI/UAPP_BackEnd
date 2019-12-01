from App.Tailwind.models import TailwindRequest
from Common.userAuthCommon import check_login, getUser
from Common.dictInfo import model_to_dict
from Common.paginator import paginator
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView


class UserTailwindRequestUnpaidListView(APIView):
    @check_login
    def get(self, request):
        '''
        获取用户的所有的未支付的请求单
        :param request:
        :return:
        '''
        user = getUser(email=request.session.get("login"))
        page = request.GET.get('page')
        unpaid_tailwind_request_list_obj = TailwindRequest.objects.filter(
            Q(initiator=user) &
            Q(status='unpaid')
        )
        unpaid_tailwind_request_list = paginator(unpaid_tailwind_request_list_obj, page)

        unpaid_tailwind_request = [model_to_dict(ut) for ut in unpaid_tailwind_request_list]

        return JsonResponse({
            'status': True,
            'unpaid_tailwind_request': unpaid_tailwind_request,
            'has_next': unpaid_tailwind_request_list.has_next(),
            'has_previous': unpaid_tailwind_request_list.has_previous()
        })
