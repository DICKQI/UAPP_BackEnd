from App.Account.models import UserInfo
from Common.userAuthCommon import check_login, getUser
from App.Account.views.esCheck import BNUZ_es_check
from django.http import JsonResponse
from rest_framework.views import APIView
import json


class StudentUserCheckView(APIView):

    @check_login
    def post(self, request):
        """
        学生认证接口
        :param request:
        :return:
        """
        try:
            user = getUser(request.session.get('login'))
            if user.student_id != 0:
                return JsonResponse({
                    'status': False,
                    'errMsg': '账号已经认证过了'
                }, status=401)
            jsonParams = json.loads((request.body).decode('utf-8'))
            stuID = jsonParams.get('username')
            password = jsonParams.get('password')
            check_result = BNUZ_es_check(stuID, password)
            if check_result:
                user.RealName = check_result['name']
                user.student_id = stuID
                user.save()
                return JsonResponse({
                    'status': True,
                    'student_id': stuID,
                    'real_name': user.RealName
                })
            else:
                return JsonResponse({
                    'status': False,
                    'errMsg': '验证失败'
                }, status=401)

        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': '错误信息：' + str(ex)
            }, status=403)
