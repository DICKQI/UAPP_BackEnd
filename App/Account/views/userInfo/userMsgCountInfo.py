from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
from App.Tailwind.models import TailwindTakeOrder, TailwindRequest, DealRate
from Common.userAuthCommon import getUser, check_login
from Common.dictInfo import model_to_dict


class MeView(APIView):

    USER_INCLUDE_FIELDS = [
        'nickname', 'id',
    ]

    @check_login
    def get(self, request):
        '''
        获取当前登录用户信息
        :param request:
        :return:
        '''

        user = getUser(request.session.get('login'))

        userResult = model_to_dict(user, fields=self.USER_INCLUDE_FIELDS)

        # 统计订单情况
        # 统计未支付的订单数量
        unpaid_number = TailwindRequest.objects.filter(
            Q(initiator=user) &
            Q(status='unpaid')
        ).count()
        # 统计等待接单订单数量
        waiting_number = TailwindRequest.objects.filter(
            Q(initiator=user) &
            Q(status='paid')
        ).count()
        # 统计(已接单)待完成订单数量
        waiting_for_finish_number = TailwindRequest.objects.filter(
            Q(initiator=user) &
            Q(status='orderT')
        ).count()
        # 统计未评价订单数量
        unrated_number = TailwindRequest.objects.filter(
            Q(initiator=user) &
            Q(status='waitR')
        ).count()
        tailwind_number = {}
        tailwind_number['unpaid_number'] = str(unpaid_number)
        tailwind_number['waiting_number'] = str(waiting_number)
        tailwind_number['waiting_for_finish_number'] = str(waiting_for_finish_number)
        tailwind_number['unrated_number'] = str(unrated_number)

        # 头像参数修改
        # if user.head_portrait:

        #     userResult['head'] = 'https://freetime-oss.oss-cn-shenzhen.aliyuncs.com/media/' + str(
        #         user.head_portrait) + '?x-oss-process=style/head_portrait'
        # else:
        #     userResult['head'] = None

        if user.user_role == '5':
            userResult['email_active'] = False
        else:
            userResult['email_active'] = True
        if user.student_id != '0':
            userResult['es_check'] = True
        else:
            userResult['es_check'] = False

        return JsonResponse({
            'status': True,
            'myself': userResult,
            'tailwind_number': tailwind_number
        })