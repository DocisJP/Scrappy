from django.db import models

class Card(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    event_date = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    source_url = models.URLField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.title or "Untitled Card"
