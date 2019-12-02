from itertools import chain
from django.db.models.fields.related import ManyToManyField, ForeignKey
from django.db.models.fields import DateTimeField
from App.Account.models import UserInfo, School


def model_to_dict(instance, fields=None, exclude=None, *args, **kwargs):
    """
        改造django.forms.models.model_to_dict()方法
        :param instance:
        :type instance: django.db.models.Model
        :param fields:  成员名称白名单（设置时将按这个名单为准，否则输出全部）
        :param exclude: 成员名称黑名单
        :return:
        为了使外键展开，ManyToMany键展开
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        value = f.value_from_object(instance)
        if not getattr(f, 'editable', False):
            continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue

        if isinstance(f, ForeignKey):
            if f.verbose_name == '订单接单人' or f.verbose_name == '订单发起人':
                user = UserInfo.objects.get(id=value)
                value = {
                    'id': value,
                    'user': user.nickname,
                    'head_portrait': ('https://freetime-oss.oss-cn-shenzhen.aliyuncs.com/media/' + user.head_portrait.name) if user.head_portrait else False
                }
            if f.verbose_name == '学校':
                value = School.objects.get(id=value).name
            # if f.verbose_name == '关联发起订单':
            #     from App.Tailwind.models import TailwindRequest
            #     value = TailwindRequest.objects.get(requestID=value)
        if isinstance(f, DateTimeField):
            data_time = str(value)
            year = data_time[0:4]
            month = data_time[5:7]
            day = data_time[8:10]
            hour = data_time[11:13]
            min = data_time[14:16]
            sec = data_time[17:19]
            value = year + "-" + month + "-" + day + " " + hour + ":" + min + ":" + sec
        if f.verbose_name == '发起单附图':
            # value = 'https://freetime-oss.oss-cn-shenzhen.aliyuncs.com/media/' + value.name
            if value.name:
                value = 'https://freetime-oss.oss-cn-shenzhen.aliyuncs.com/media/' + value.name
            else:
                value = False
        data[f.name] = value
    return data