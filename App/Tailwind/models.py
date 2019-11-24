from django.db import models
from App.Account.models import UserInfo
from django.utils.timezone import now


# 有闲app后端核心模块
# Create your models here.

class TailwindRequest(models.Model):
    '''有闲发起单数据库模型'''
    STATUS_CHOICES = (
        ('unpaid', '未支付'),
        ('paid', '等待接单'),  # 已支付
        ('orderT', '已被接单'),
        ('waitR', '等待评价'),
        ('accomplish', '已完成'),
        ('cancel', '订单取消'),
    )

    TYPE_CHOICE = (
        ('deliver', '代送'),
        ('work', '代办')
    )

    requestID = models.BigIntegerField(verbose_name='发起单编号', primary_key=True, blank=False, unique=True, default=1)
 
    initiator = models.ForeignKey(UserInfo, verbose_name='订单发起人', on_delete=models.CASCADE)

    taskContent = models.TextField(verbose_name='任务内容', default='', blank=False)

    beginTime = models.DateTimeField(verbose_name='开始时间', default=now, blank=False)

    endTime = models.DateTimeField(verbose_name='截止时间', blank=False)

    serviceType = models.CharField(verbose_name='服务类型', max_length=100, choices=TYPE_CHOICE, default='deliver',
                                   blank=False)

    beginPlace = models.CharField(verbose_name='开始地点', default='', max_length=100, blank=False)

    endPlace = models.CharField(verbose_name='结束地点', default='', max_length=100, blank=True)  # 代办任务的时候，结束地点可为空

    status = models.CharField(verbose_name='状态', choices=STATUS_CHOICES, max_length=100, default='unpaid', blank=False)

    money = models.FloatField(verbose_name='金额', blank=False, default=0.0)

    img = models.ImageField(verbose_name='发起单附图', default='', blank=True, upload_to='tailwind')

    class Meta:
        verbose_name = '有闲发起单'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'Tailwind_TailwindRequest'
        ordering = ['-beginTime']

    def __str__(self):
        return self.initiator.nickname


class TailwindTakeOrder(models.Model):
    '''有闲订单数据库模型'''

    STATUS_CHOICES = (
        ('unaccomplished', '未完成'),
        ('accomplished', '已完成')
    )

    takeID = models.BigIntegerField(verbose_name='订单编号', primary_key=True, blank=False, unique=True, default=1)

    mandatory = models.ForeignKey(UserInfo, verbose_name='订单接单人', on_delete=models.CASCADE)

    tailwind = models.ForeignKey(TailwindRequest, verbose_name='关联发起订单', on_delete=models.CASCADE)

    status = models.CharField(verbose_name='订单状态', choices=STATUS_CHOICES, max_length=100, blank=False,
                              default='unaccomplished')

    create_time = models.DateTimeField(verbose_name='创建时间', default=now, blank=False)

    end_time = models.DateTimeField(verbose_name='结束时间', blank=True)

    class Meta:
        verbose_name = '有闲接受订单'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'Tailwind_TailwindTakeOrder'
        ordering = ['-create_time']

    def __str__(self):
        return self.mandatory.nickname


class DealRate(models.Model):
    '''有闲交易互评数据库模型'''

    RATE_STATUS = (
        ('un_reviewed', '未评价'),
        ('Party_A_has_reviewed', '甲方已评'),
        ('Party_B_has_reviewed', '乙方已评'),
        ('Two_Size_has_reviewed', '双方已评')
    )

    relateTailwindTakeOrder = models.ForeignKey(TailwindTakeOrder, verbose_name='关联的有闲订单', on_delete=models.CASCADE)

    create_time = models.DateTimeField(verbose_name='创建时间', default=now, blank=False)

    FirstPartyRate = models.CharField(verbose_name='甲方评价', default='', blank=False, max_length=230)

    SecondPartyRate = models.CharField(verbose_name='乙方评价', default='', blank=False, max_length=230)

    status = models.CharField(verbose_name='评价表状态', choices=RATE_STATUS, blank=False, max_length=100, default='un_reviewed')

    class Meta:
        verbose_name = '有闲交易互评'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'Tailwind_DealRate'

    def __str__(self):
        return self.relateTailwindTakeOrder.takeID

