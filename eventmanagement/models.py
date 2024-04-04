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
