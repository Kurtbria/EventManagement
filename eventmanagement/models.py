from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Ticket(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    ticket_number = models.CharField(max_length=8)
    ticket_code = models.CharField(max_length=12)
    number_of_tickets = models.IntegerField(default=1)
    date = models.DateTimeField(default=timezone.now)
    purchase_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.full_name} - Ticket: {self.ticket_number}'


class UserActivity(models.Model):
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    request_url = models.CharField(max_length=255, blank=True, null=True)
    http_method = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"User Activity - {self.request_url}"

    class Meta:
        verbose_name_plural = "User Activities"





  