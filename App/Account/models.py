from django.db import models
from django.utils.timezone import now


# Create your models here.
class School(models.Model):
    '''学校信息数据库模型'''
    name = models.CharField(verbose_name='学校名', blank=False, default='', unique=True, max_length=100)

    abbreviation = models.CharField(verbose_name='学校名缩写', blank=False, default='', max_length=100)

    user_number = models.BigIntegerField(verbose_name='学校用户数', default=0, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '学校'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'Account_School'


class UserPassword(models.Model):
    '''账户密码表'''
    password = models.CharField(verbose_name='用户密码', max_length=1000, blank=False, default=None)

    class Meta:
        verbose_name = '用户密码'
        verbose_name_plural = verbose_name
        db_table = 'Account_UserPassword'


class UserInfo(models.Model):
    '''主账户数据库模型'''
    roles = {
        ('515400', '总管理员'),
        ('99', 'VIP用户'),
        ('4', '普通用户(已验证邮箱)'),
        ('5', '普通用户(未验证邮箱)'),
        ('6', '黑名单用户'),
    }
    '''基础信息'''

    email = models.EmailField(verbose_name='邮箱', blank=False, default=None, unique=True)

    nickname = models.CharField(verbose_name='用户昵称', max_length=20, default=None, blank=False, unique=True)

    password = models.ForeignKey(UserPassword, verbose_name='密码', default='', blank=False, on_delete=models.CASCADE)

    joined_date = models.DateTimeField(verbose_name='注册时间', default=now)

    '''详细信息'''

    signature = models.CharField(verbose_name='个性签名', max_length=100, default='这个人很懒，什么都没写...', blank=True)

    user_role = models.CharField(verbose_name='用户身份', max_length=6, choices=roles, default=5)

    student_id = models.BigIntegerField(verbose_name='学号', default=0, blank=True)

    RealName = models.CharField(verbose_name='真实姓名', max_length=100, default=None, null=True, blank=True)

    age = models.IntegerField(verbose_name='年龄', blank=True, default=1)

    head_portrait = models.ImageField(verbose_name='头像', max_length=2000, blank=True, upload_to='head_portrait')

    credit_score = models.IntegerField(verbose_name='信用分', default=500)

    from_school = models.ForeignKey(School, verbose_name='学校', on_delete=models.CASCADE, blank=True)

    '''记录信息'''
    last_login_time = models.DateTimeField(verbose_name='最后登录时间', default=now)

    TimesOfPraise = models.IntegerField(verbose_name='好评次数', default=0)

    TimesOfBadEvaluation = models.IntegerField(verbose_name='差评次数', default=0)

    TimesOfTake = models.IntegerField(verbose_name='接单次数', default=0)

    TimesOfRequest = models.IntegerField(verbose_name='发单次数', default=0)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户列表'
        ordering = ['-joined_date']
        db_table = 'Account_UserInfo'


class EmailVerifyRecord(models.Model):
    '''邮箱验证码'''
    type = {
        ('active', '激活'),
        ('forget', '找回密码')
    }
    status = {
        ('used', '已使用'),
        ('not_use', '未使用')
    }
    code = models.CharField(verbose_name='验证码', unique=True, max_length=20)
    email = models.CharField(verbose_name='邮箱', max_length=50)

    send_type = models.CharField(verbose_name='验证类型', choices=type, max_length=10)
    code_status = models.CharField(verbose_name='验证码使用情况', max_length=10, choices=status, default='not_use')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
        db_table = 'Account_EmailVerifyCode'

    def __str__(self):
        return self.email + " " + self.code_status


class UserConfig(models.Model):
    '''账户个性化设置'''
    relateUser = models.ForeignKey(UserInfo, verbose_name='关联主账户', on_delete=models.CASCADE)

    dormitory = models.CharField(verbose_name='宿舍楼', default=None, null=True, blank=True, max_length=100)

    commonAcademicBuilding = models.TextField(verbose_name='常用教学楼', default='', null=True, blank=True)
