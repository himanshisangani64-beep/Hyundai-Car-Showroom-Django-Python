# secure_session_middleware.py
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class PreventBackMiddleware(MiddlewareMixin):
    """
    Prevent users from accessing cached pages after logout
    and redirect unauthorized access to login/home.
    """

    def process_response(self, request, response):
        # Add headers to prevent caching
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def process_request(self, request):
        # Allow login, logout, registration pages without session
        allowed_urls = [
            '/login/', '/logincheck/', '/registration/', '/regidata/',
            '/logout/', '/admin/', '/static/','/home/',
        ]
        path = request.path
        if any(path.startswith(url) for url in allowed_urls):
            return None  # Allow access

        # If user not logged in, redirect to login/home
        if not request.session.get('cname') and not request.user.is_authenticated:
            return redirect('home')  # or 'home' for normal users

        return None
