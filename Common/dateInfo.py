import datetime


def get_three_month_ago():
    """
    获取三个月前的datetime对象
    :return: type datetime.datetime
    """
    datetimeNow = datetime.datetime.now()
    three_month_ago_delta = datetime.timedelta(days=90)
    three_month_ago = datetimeNow - three_month_ago_delta
    return three_month_ago


def generateFormatTime():
    dt = datetime.datetime.now()
    time = str(dt.year) + (str(dt.month) if dt.month > 9 else '0' + str(dt.month)) + (
        str(dt.day) if dt.day > 9 else '0' + str(dt.day)) + (
               str(dt.hour) if dt.hour > 9 else '0' + str(dt.hour)) + (
               str(dt.minute) if dt.minute > 9 else '0' + str(dt.minute))
    return time
