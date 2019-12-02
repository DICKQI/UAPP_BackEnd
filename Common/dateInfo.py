import datetime


def get_three_month_ago():
    """
    获取三个月前的datetime对象
    :return: type datetime.datetime
    """
    datetimeNow = datetime.datetime.now()
    month = datetimeNow.month
    year = datetimeNow.year
    if month > 3:
        month -= 3
    else:
        year -= 1
        month = 12 - 3 + month
    year = str(year)
    month = str(month)
    three_month_ago = year + '-' + month + '-' + str(
        datetimeNow.day) + ' ' + str(datetimeNow.hour) + ':' + str(datetimeNow.minute) + ":" + str(
        datetimeNow.second)
    return three_month_ago
