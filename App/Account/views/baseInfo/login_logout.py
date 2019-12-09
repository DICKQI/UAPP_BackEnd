from rest_framework.views import APIView
from App.Account.models import UserInfo, UserPassword
from App.Log.models import LoginLog
from Common.userAuthCommon import check_login, getUser
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from django.db.models import Q
import json


class AccountBaseView(APIView):

    # @check_login
    def get(self, request):
        '''
        用于检查是否登录
        :param request:
        :return:
        '''
        if request.session.get('login', None):
            return JsonResponse({
                'status': True,
                'id': getUser(request.session.get('login')).id
            })
        else:
            return JsonResponse({
                'status': False,
                'errMsg': '你还未登录'
            }, status=401)

    def post(self, request):
        '''
        登录账户
        :param request:
        :return:
        '''
        try:
            jsonParams = json.loads((request.body).decode('utf-8'))
            user = UserInfo.objects.filter(
                Q(email=jsonParams.get('email')) |
                Q(id=jsonParams.get('id'))
            )
            if not user.exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '无此用户'
                }, status=401)
            user = user[0]
            if user.user_role == '6':
                return JsonResponse({
                    'status': False,
                    'errMsg': '用户已被封禁'
                }, status=401)
            db_password = user.password.password
            if check_password(jsonParams.get('password'), db_password):
                # 在session中记录登录
                request.session['login'] = user.email
                '''记录登录信息'''
                user.last_login_time = now
                ip = request.META['REMOTE_ADDR']
                device = jsonParams.get('device')
                LoginLog.objects.create(
                    ip=ip,
                    user=user,
                    login_device=device
                )
                return JsonResponse({
                    'status': True,
                    'id': user.id,
                    'nickname': user.nickname,
                    'email': user.email
                })
            return JsonResponse({
                'status': False,
                'errMsg': '密码错误'
            }, status=401)

        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': '错误信息：' + str(ex)
            }, status=403)

    @check_login
    def delete(self, request):
        '''
        登出账户
        :param request:
        :return:
        '''
        user = getUser(request.session.get('login'))
        # 删除服务器session
        request.session['login'] = None
        return JsonResponse({
            'status': True,
            'id': user.id
        })
