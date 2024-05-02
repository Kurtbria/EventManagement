from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.URLField()
    description = models.TextField()
    date = models.DateField()
    organizer = models.CharField(max_length=100)
    ticket_link = models.URLField()

    def __str__(self):
        return self.title

class Ticket(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    ticket_number = models.CharField(max_length=8)
    ticket_code = models.CharField(max_length=12)
    number_of_tickets = models.IntegerField(default=1)
