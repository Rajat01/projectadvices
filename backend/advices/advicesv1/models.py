from __future__ import unicode_literals

from django.db import models




class Questions(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=1000, blank=True, default='')








# Create your models here.
