from django.utils.deprecation import MiddlewareMixin
from .models import UserActivity, UserRecord
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class UserActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT')
        ip_address = request.META.get('REMOTE_ADDR')
        request_url = request.get_full_path()
        http_method = request.method

        logger.info("User Agent: %s", user_agent)
        logger.info("IP Address: %s", ip_address)
        logger.info("Request URL: %s", request_url)
        logger.info("HTTP Method: %s", http_method)

        print("User Agent:", user_agent)
        print("IP Address:", ip_address)
        print("Request URL:", request_url)
        print("HTTP Method:", http_method)

