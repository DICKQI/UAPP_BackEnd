from django.db import models
from django.utils.timezone import now
from App.Account.models import UserInfo

class LoginLog(models.Model):

    device = (
        ('android', '安卓'),
        ('apple', '苹果'),
        ('web', '网页'),
        ('weapp', '微信小程序')
    )

    '''记录用户登录信息'''
    ip = models.CharField(verbose_name='用户ip', max_length=200, blank=False, default='')

    user = models.ForeignKey(UserInfo, verbose_name='关联用户', on_delete=models.CASCADE, blank=False, default='')

    login_device = models.CharField(verbose_name='登录端', blank=False, default='web', choices=device, max_length=100)

    loginTime = models.DateTimeField(verbose_name='登录时间', default=now)

    def __str__(self):
        return self.ip

    class Meta:
        db_table = 'Log_LoginLog'