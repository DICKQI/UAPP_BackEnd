from django.urls import path
from .tailwindRequestInfo import UserTailwindRequestView


app_name = 'user_tailwind'

urlpatterns = [
    # 用户对请求单的操作
    path('request/', UserTailwindRequestView.as_view(), name='myself_user_tailwind_request'),
    path('request/<int:tid>/', UserTailwindRequestView.as_view(), name='user_tailwind_request'),
    # 用户对接受当的操作
]