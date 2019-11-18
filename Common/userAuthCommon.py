from django.http import JsonResponse
from App.Account.models import UserInfo


def check_login(func):
    '''
    用于检查用户是否登录的装饰器
    :param func:
    :return:
    '''
    def wrapper(self, request, *args, **kwargs):
        if request.session.get('login') != None:
            user = getUser(request.session.get('login'))
            '''检测是否为黑名单用户，黑名单用户限制一切功能'''
            if user.user_role == '6':
                return JsonResponse({
                    'errMsg': '账号已被封禁，请联系管理员',
                    'status': False
                }, status=401)
            return func(self, request, *args, **kwargs)
        else:
            return JsonResponse({
                'status': False,
                'errMsg': '你还未登录'
            }, status=401)

    return wrapper


def getUser(email):
    '''
    通过获取request的session中email来获取用户对象
    :param email:
    :return:
    '''
    return UserInfo.objects.get(email=email)


def checkStudent(func):
    '''
    学生认证
    :param func:
    :return:
    '''
    def wrapper(self, request, *args, **kwargs):
        user = getUser(request.session.get('login'))
        if user.user_role != '515400':
            if user.student_id == '0':
                print(2)
                return JsonResponse({
                    'status': False,
                    'errMsg': '你还没有进行学生认证，请完成认证后再进行操作'
                })
        return func(self, request, *args, **kwargs)

    return wrapper