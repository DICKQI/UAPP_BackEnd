from App.Tailwind.models import TailwindRequest
from Common.userAuthCommon import check_login, getUser
from Common.dictInfo import model_to_dict
from Common.paginator import paginator
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView


class UserTailwindRequestWaitRateListView(APIView):

    def get(self, request):
        '''

        :param request:
        :return:
        '''
        user = getUser(email=request.session.get("login"))
        page = request.GET.get('page')
        waitRate_tailwind_request_list_obj = TailwindRequest.objects.filter(
            Q(initiator=user) &
            Q(status='waitR')
        )
        waitRate_tailwind_request_list = paginator(waitRate_tailwind_request_list_obj, page)

        waitRate_tailwind_request = [model_to_dict(wrt) for wrt in waitRate_tailwind_request_list]

        return JsonResponse({
            'status': True,
            'waitRate_tailwind_request': waitRate_tailwind_request,
            'has_next': waitRate_tailwind_request_list.has_next(),
            'has_previous': waitRate_tailwind_request_list.has_previous()
        })
