from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class AjaxAuthenticationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (request.is_ajax()):
            if (response.status_code == 302):
                response.status_code = 403
        return response