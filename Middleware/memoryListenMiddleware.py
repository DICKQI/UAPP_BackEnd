import os
import psutil

from django.utils.deprecation import MiddlewareMixin


def show_memory_info(hint):
    pid = os.getpid()
    p = psutil.Process(pid)
    info = p.memory_full_info()
    memory = info.uss / 1024. / 1024
    print('{} memory used: {}MB'.format(hint, memory))


class MemoryListenMiddleware(MiddlewareMixin):

    def process_request(self, request):
        show_memory_info('request process')
        return None

    def process_response(self, request, response):
        show_memory_info('response process')
        return response
