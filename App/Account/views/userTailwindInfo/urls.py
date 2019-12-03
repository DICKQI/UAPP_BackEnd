from django.urls import path
from .userTailwindBaseInfo import *


app_name = 'user_tailwind'

urlpatterns = [
    # 用户对请求单的操作
    path('request/', UserTailwindRequestView.as_view(), name='myself_user_tailwind_request'),  # 新建，查看（列表）
    path('request/<int:tid>/', UserTailwindRequestView.as_view(), name='user_tailwind_request'),  # 加图，取消
    # 用户对接受单的操作
    path('take/', UserTailwindTakeOrderView.as_view(), name='user_tailwind_takeOrder_info'),  # 查看
    path('take/<int:rid>/', UserTailwindTakeOrderView.as_view(), name='user_tailwind_takeOrder'),  # 接单
]
