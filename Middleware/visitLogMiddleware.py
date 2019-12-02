from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.utils.timezone import now


class VisitLogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        return None