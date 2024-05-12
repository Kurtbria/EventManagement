from django.utils.deprecation import MiddlewareMixin
from .models import UserActivity, UserRecord

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

'''class UserRecordActivity(MiddlewareMixin):
    def process_record(self, request):
        user_browser = request.META.get('HTTP_USER_AGENT')
        ip_address = request.META.get('IP_ADDR')
        request_url = request.META.get_full_path()
        http_method = request.get_full_path()


        UserRecord.objects.create(
            user_browser = user_browser,
            ip_address = ip_address,
            request_url = request_url,
            http_method = http_method,

        )'''
