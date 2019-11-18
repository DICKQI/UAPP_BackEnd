from django.contrib import admin
from .models import TailwindRequest, TailwindTakeOrder


# Register your models here.

@admin.register(TailwindRequest)
class TailwindRequestAdmin(admin.ModelAdmin):
    list_per_page = 50
    search_fields = ['requestID']
    list_filter = ['serviceType', 'status']
    list_display = ['requestID', 'serviceType', 'status', 'beginTime', 'endTime', 'beginPlace', 'endPlace', 'money']


@admin.register(TailwindTakeOrder)
class TailwindTakeOrderAdmin(admin.ModelAdmin):
    list_per_page = 50
    search_fields = ['takeID']
    list_filter = ['status']
    list_display = ['takeID', 'status', 'create_time', 'end_time']
