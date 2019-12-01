from App.Tailwind.models import TailwindRequest
from Common.userAuthCommon import check_login, getUser
from Common.dictInfo import model_to_dict
from Common.paginator import paginator
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView


class UserTailwindRequestPaidListView(APIView):

    @check_login
    def get(self, request):
        '''
        获取用户的所有的已支付未被接单的请求单
        :param request:
        :return:
        '''
        user = getUser(email=request.session.get("login"))
        page = request.GET.get('page')
        paid_tailwind_request_list_obj = TailwindRequest.objects.filter(
            Q(initiator=user) &
            Q(status='paid')
        )
        paid_tailwind_request_list = paginator(paid_tailwind_request_list_obj, page)

        paid_tailwind_request = [model_to_dict(pt) for pt in paid_tailwind_request_list]

        return JsonResponse({
            'status': True,
            'paid_tailwind_request': paid_tailwind_request,
            'has_next': paid_tailwind_request_list.has_next(),
            'has_previous': paid_tailwind_request_list.has_previous()
        })

