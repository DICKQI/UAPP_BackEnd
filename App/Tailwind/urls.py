from django.urls import path
from .views import *

app_name = 'Tailwind'

urlpatterns = [
    path('list/', TailwindRequestListView.as_view(), name='TailwindRequestList'),
]