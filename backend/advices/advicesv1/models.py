from __future__ import unicode_literals
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import User


class Questions(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=1000, blank=True, default='')
    up_votes = models.IntegerField(blank=True, default=0)
    asked_by = models.ForeignKey(User, related_name='question_user', null=True, default=None, on_delete=models.CASCADE)

    def __unicode__(self):
        return "created: {0} question: {1} up_votes: {2}".format(self.created, self.question, self.up_votes)


class Advices(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    advice_content = models.CharField(max_length=1000, blank=True, default='')
    question = models.ForeignKey(Questions)
    up_votes = models.IntegerField(blank=True, default=0)

    advised_by = models.ForeignKey(User, related_name='advice_user', null=True, default=None, on_delete=models.CASCADE)

    def __unicode__(self):
        return "created: {0} advice_content: {1} question: {2}".format(self.created, self.advice_content,
                                                                       self.question_id)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class Stories(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    story_content = models.CharField(max_length=500)

# Create your models here.
