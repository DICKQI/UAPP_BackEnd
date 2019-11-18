from App.Tailwind.models import TailwindRequest
from App.Account.models import UserInfo
from django.http import JsonResponse
from Common.paginator import paginator
from Common.dictInfo import model_to_dict
from Common.userAuthCommon import check_login, getUser, checkStudent
from rest_framework.views import APIView
import json, datetime


class UserTailwindRequestView(APIView):
    COMMON_FIELDS = [
        'requestID', 'taskContent', 'beginTime', 'endTime',
        'money', 'serviceType', 'status'
    ]

    @check_login
    @checkStudent
    def get(self, request, uid=0):
        '''
        获得用户发起的订单
        :param request:
        :return:
        '''
        try:
            if uid == 0:
                user = getUser(email=request.session.get('login'))
            else:
                user = UserInfo.objects.filter(id=uid)
                if not user.exists():
                    return JsonResponse({
                        'status': False,
                        'errMsg': '用户不存在'
                    }, status=404)
            page = request.GET.get('page')
            tailwindObj = TailwindRequest.objects.filter(initiator=user)
            tailwindList = paginator(tailwindObj, page)
            tailwind = [model_to_dict(t, fields=self.COMMON_FIELDS) for t in tailwindList]
            return JsonResponse({
                'status': True,
                'tailwind': tailwind
            })
        except:
            return JsonResponse({
                'status': False,
                'errMsg': '出现未知错误'
            }, status=403)

    @check_login
    @checkStudent
    def post(self, request):
        '''
        用户发起订单
        :param request:
        :return:
        '''
        try:
            user = getUser(email=request.session.get('login'))
            jsonParam = json.loads(request.body)

            taskContent = jsonParam.get('content')
            serviceType = jsonParam.get('type')
            beginPlace = jsonParam.get('begin place')
            endPlace = jsonParam.get('end place')
            money = float(jsonParam.get('money'))
            endTime = datetime.datetime.strptime(jsonParam.get('end time'), '%Y-%m-%d %H:%M:%S')

            newTailwindRequest = TailwindRequest.objects.create(

            )

        except:
            return JsonResponse({
                'status': False,
                'errMsg': '出现未知错误'
            }, status=403)

    @check_login
    @checkStudent
    def put(self, requests, tid):
        '''
        用户为发起单添加图片
        :param requests:
        :param tid:
        :return:
        '''
        try:
            pass
        except:
            return JsonResponse({
                'status': False,
                'errMsg': '出现未知错误'
            }, status=403)

    def generateRequestID(self):
        dt = datetime.datetime.now()
        time = str(dt.year) + str(dt.month) + str(dt.day) + (
            str(dt.hour) if dt.hour > 9 else '0' + str(dt.hour)) + (
                       str(dt.minute) if dt.minute > 9 else '0' + str(dt.minute)) + str(dt.second)

