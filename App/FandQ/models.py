from django.db import models
from django.utils.timezone import now
from App.Account.models import UserInfo
# Create your models here.

class Notice(models.Model):
    '''公告数据库模型'''
    admin = models.ForeignKey(UserInfo, verbose_name='管理员', on_delete=models.CASCADE)

    title = models.CharField(verbose_name='标题', max_length=20, default='', blank=False)

    content = models.TextField(verbose_name='内容', default='', blank=False)

    last_mod_time = models.DateTimeField(verbose_name='最后修改时间', default=now)

    class Meta:
        ordering = ['-last_mod_time']
        db_table = 'Notice'
        verbose_name = '公告'
        verbose_name_plural = '公告列表'

    def __str__(self):
        return self.title

class Feedback(models.Model):
    '''反馈信息数据库模型'''
    UpTime = models.DateTimeField(verbose_name='提交时间', default=now)

    content = models.TextField(verbose_name='内容', blank=False, default=None)

    contact = models.CharField(verbose_name='联系方式', blank=False, max_length=100, default=None)

    class Meta:
        ordering = ['-UpTime']
        db_table = 'Feedback'
        verbose_name = '反馈信息'
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.contact