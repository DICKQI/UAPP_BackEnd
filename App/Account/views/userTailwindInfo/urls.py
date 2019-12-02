from django.urls import path
from .userTailwindBaseInfo import *
from .userTailwindRequestDetailList import *

app_name = 'user_tailwind'

urlpatterns = [
    # 用户对请求单的操作
    path('request/', UserTailwindRequestView.as_view(), name='myself_user_tailwind_request'),  # 新建，查看
    path('request/<int:tid>/', UserTailwindRequestView.as_view(), name='user_tailwind_request'),  # 加图，取消
    # 用户请求单详情
    path('request/detail/unpaid/', UserTailwindRequestUnpaidListView.as_view(),
         name='user_tailwind_request_unpaid_list'),
    path('request/detail/paid/', UserTailwindRequestPaidListView.as_view(), name='user_tailwind_request_paid_list'),
    path('request/detail/take/', UserTailwindRequestOrderTListView.as_view(), name='user_tailwind_request_orderT_list'),
    path('request/detail/wait_rate/', UserTailwindRequestWaitRateListView.as_view(),
         name='user_tailwind_request_wait_rate_list'),
    # 用户对接受单的操作
    path('take/', UserTailwindTakeOrderView.as_view(), name='user_tailwind_takeOrder_info'),  # 查看
    path('take/<int:rid>/', UserTailwindTakeOrderView.as_view(), name='user_tailwind_takeOrder'),  # 接单
]
