from datetime import datetime
from django.db import models

class Ticket(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    ticket_number = models.CharField(max_length=8)
    ticket_code = models.CharField(max_length=12)
    number_of_tickets = models.IntegerField(default=1)
    date = models.DateTimeField(default=datetime.now())
