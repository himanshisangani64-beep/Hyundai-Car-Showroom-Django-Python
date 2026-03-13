from django.utils.deprecation import MiddlewareMixin

class NoCacheMiddleware(MiddlewareMixin):
    """ Prevent browser from caching pages (fixes back/forward after logout) """
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
