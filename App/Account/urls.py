from django.urls import path
from django.conf.urls import include
from .views import *

app_name = 'Account'
urlpatterns = [
    # baseInfo
    path('', AccountBaseView.as_view(), name='login_logout_checkLogin'),
    path('register/', RegisterView.as_view(), name='register'),
    # userInfo
    path('me/', MeView.as_view(), name='user_tailwind_count'),
    path('dashboard/', UserInfoView.as_view(), name='myself_dashboard'),
    path('dashboard/<int:uid>/', UserInfoView.as_view(), name='other_dashboard'),
    # tailwindInfo
    path('tailwind/', include('App.Account.views.userTailwindInfo.urls', namespace='user_tailwind')),

]
