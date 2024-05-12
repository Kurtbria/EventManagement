# middleware.py

from django.utils.deprecation import MiddlewareMixin
from .models import UserActivity  

class UserActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT')
        ip_address = request.META.get('REMOTE_ADDR')
        request_url = request.get_full_path()
        http_method = request.method

        UserActivity.objects.create(
            user_agent=user_agent,
            ip_address=ip_address,
            request_url=request_url,
            http_method=http_method
        )
