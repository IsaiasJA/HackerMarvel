from django.db import models
from django.conf import settings

# Create your models here.
class Heroe(models.Model):
    url = models.URLField()
    name = models.TextField(blank=True)
    description = models.TextField(blank=True)
    comic = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.ForeignKey('links.Heroe', related_name='votes', on_delete=models.CASCADE)