from django.urls import path
from .tailwindRequestInfo import UserTailwindRequestView


app_name = 'user_tailwind'

urlpatterns = [
    path('request/', UserTailwindRequestView.as_view(), name='myself_user_tailwind_request'),
    path('request/<int:uid>/', UserTailwindRequestView.as_view(), name='user_tailwind_request'),
]