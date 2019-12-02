from rest_framework.views import APIView
from App.Account.models import UserInfo, School, UserPassword, UserConfig
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import random
import json


def randomID():
    '''
    生成随机不重复的id
    :return:
    '''
    newid = random.randint(10000000, 999999999)
    while UserInfo.objects.filter(id=newid).exists():
        newid = random.randint(10000000, 999999999)
    return newid


class RegisterView(APIView):
    def post(self, request):
        '''注册账户'''
        params = request.body
        jsonParams = json.loads(params.decode('utf-8'))
        # 检查参数合法性
        user = UserInfo.objects.filter(email__exact=jsonParams.get('email'))
        if user.exists():
            return JsonResponse({
                'status': False,
                'errMsg': '邮箱已经被注册'
            }, status=401)
        user = UserInfo.objects.filter(nickname__exact=jsonParams.get('nickname'))
        if user.exists():
            return JsonResponse({
                'status': False,
                'errMsg': '昵称已经被人抢先用啦'
            }, status=401)
        school = School.objects.filter(abbreviation__exact=str(jsonParams.get('school')).upper())
        if not school.exists():
            return JsonResponse({
                'status': False,
                'errMsg': '学校不存在'
            }, status=401)
        school = school[0]

        # 密码转码
        hash_password = make_password(jsonParams.get('password'))
        # 随机ID
        newid = randomID()
        # 创建密码
        newPassword = UserPassword.objects.create(
            password=hash_password
        )
        # 创建账户
        newUser = UserInfo.objects.create(
            id=newid,
            password=newPassword,
            email=jsonParams.get('email'),
            nickname=jsonParams.get('nickname'),
            from_school=school
        )
        # 对应学校账户+1
        school.user_number += 1
        school.save()

        # 注册账户的时候同时创建一个用户个性化设置的对象
        UserConfig.objects.create(relateUser=newUser)

        return JsonResponse({
            'status': True,
            'id': newUser.id,
            'email': newUser.email,
            'nickname': newUser.nickname,
        })
