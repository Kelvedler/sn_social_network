import logging
from datetime import datetime
from django.http import JsonResponse

from main.utils.common import get_request_ip

logger = logging.getLogger(__name__)


class Logging(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = datetime.now()
        response = self.get_response(request)
        request_time = datetime.now() - start
        logger.info('HTTP {method} {ip} {path} {code} {time:.3f}s'
                    .format(method=request.META['REQUEST_METHOD'],
                            ip=get_request_ip(request),
                            path=request.META['PATH_INFO'],
                            code=response.status_code,
                            time=request_time.total_seconds()))
        return response


class UnexpectedError(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    @staticmethod
    def process_exception(request, exception):
        logger.exception(exception)
        return JsonResponse({'error': ['internal']}, status=500)
