from rest_framework.views import APIView
from App.Account.models import UserInfo
from App.Tailwind.models import TailwindRequest, TailwindTakeOrder
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from Common.dictInfo import model_to_dict
from Common.userAuthCommon import getUser, check_login


class UserInfoView(APIView):
    INCLUDE_FIELDS = [
        'id', 'email', 'nickname', 'last_login_time', 'signature', 'student_id',
        'from_school', 'credit_score', 'TimesOfPraise', 'TimesOfBadEvaluation'
    ]


    @check_login
    def get(self, request, uid=0):
        '''
        用户主页（用户详细信息）
        :param request:
        :param uid:
        :return:
        '''
        if uid == 0:
            # 查看自己的信息
            user = getUser(request.session.get('login'))
            MYSELF_FIELDS = [
                'RealName', 'age', 'joined_date', 'TimesOfTake', 'TimesOfRequest'
            ]
            self.INCLUDE_FIELDS += MYSELF_FIELDS
        else:
            # 查看他人的信息
            user = UserInfo.objects.filter(id=uid)
            if not user.exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '用户不存在'
                }, status=404)
            user = user[0]
        userInformation = model_to_dict(user, fields=self.INCLUDE_FIELDS)
        for i in user.roles:
            if i[0] == user.user_role:
                userInformation['role'] = i[1]
                break
        if user.head_portrait:
            userInformation['head_portrait'] = 'https://freetime-oss.oss-cn-shenzhen.aliyuncs.com/media/' + str(user.head_portrait)
        else:
            userInformation['head_portrait'] = False
        return JsonResponse({
            'status': True,
            'information': userInformation
        })

    @check_login
    def post(self, request):
        '''
        新增/更换头像
        :param request:
        :return:
        '''
        try:
            user = getUser(email=request.session.get('login'))
            head_portrait = request.FILES.get('img')
            user.head_portrait = head_portrait
            user.save()
            return JsonResponse({
                'status': False,
                'id': user.id
            })
        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': '错误信息：' + str(ex)
            })


    @check_login
    def put(self, request):
        '''
        用户修改信息
        :param request:
        :return:
        '''
        try:
            pass
        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': '错误信息：' + str(ex)
            })

