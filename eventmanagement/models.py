from django.db import models
from django.utils import timezone

class Ticket(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    ticket_number = models.CharField(max_length=8)
    ticket_code = models.CharField(max_length=12)
    number_of_tickets = models.IntegerField(default=1)
    date = models.DateTimeField(default=timezone.now)
    purchase_datetime = models.DateTimeField(default=timezone.now)
