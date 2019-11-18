from django.contrib import admin
from .models import UserInfo, School

@admin.register(UserInfo)
class AdminUserInfo(admin.ModelAdmin):

    list_per_page = 50
    search_fields = ['email', 'nickname']
    list_filter = ['user_role']
    list_display = ['nickname', 'email', 'student_id', 'credit_score', 'last_login_time']

@admin.register(School)
class AdminSchool(admin.ModelAdmin):

    list_per_page = 50
    search_fields = ['name']
    list_display = ['name', 'abbreviation', 'user_number']
