from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginator(obj, page):
    '''
    自定义通用分页器
    :param obj:
    :param page:
    :return:
    '''
    objPage = Paginator(obj, 10)
    try:
        objList = objPage.page(page)
    except PageNotAnInteger:
        objList = objPage.page(1)
    except EmptyPage:
        objList = objPage.page(1)
    return objList
