from django.contrib import admin
from .models import TailwindRequest, TailwindTakeOrder


# Register your models here.

def make_paid(modeladmin, request, queryset):
    queryset.update(status='paid')

make_paid.short_description = '设置所选为已支付待接单'

@admin.register(TailwindRequest)
class TailwindRequestAdmin(admin.ModelAdmin):
    list_per_page = 50
    search_fields = ['requestID']
    list_filter = ['serviceType', 'status']
    list_display = ['requestID', 'serviceType', 'status', 'beginTime', 'endTime', 'beginPlace', 'endPlace', 'money']
    actions = [make_paid]

@admin.register(TailwindTakeOrder)
class TailwindTakeOrderAdmin(admin.ModelAdmin):
    list_per_page = 50
    search_fields = ['takeID']
    list_filter = ['status']
    list_display = ['takeID', 'status', 'create_time', 'end_time']
