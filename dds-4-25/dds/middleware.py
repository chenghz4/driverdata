from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django import http

class DenyFreeAPIMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated() and not request.user.is_staff:
            if 'api' in request.path:
                try:
                    if not request.user.customer.has_active_subscription():
                        return HttpResponse("Subscription required to access API")
                except ObjectDoesNotExist:
                    return HttpResponse("Subscription required to access API")

class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
         

        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin']  = '*'
        response['Access-Control-Allow-Credentials']  = 'true'
        return response