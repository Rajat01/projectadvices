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
    asked_by = models.ForeignKey(User, related_name='question_user', null=True, default=None, on_delete=models.CASCADE)
    upvote_by = models.ManyToManyField(User, default=None, related_name='advicesv1_upvote_question')
    is_anonymously_asked = models.BooleanField(default=False)

    def __unicode__(self):
        return "created: {0} question: {1} asked_by: {2} upvote_by: {3}".format(self.created, self.question,
                                                                                self.asked_by, self.upvote_by)


class Advices(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    advice_content = models.CharField(max_length=1000, blank=True, default='')
    question = models.ForeignKey(Questions, related_name='advicesv1_advices', null=True, default=None)
    advised_by = models.ForeignKey(User, related_name='advice_user', null=True, default=None, on_delete=models.CASCADE)
    upvote_by = models.ManyToManyField(User, default=None, related_name='advicesv1_upvote_advice')
    downvote_by = models.ManyToManyField(User, default=None, related_name='advicesv1_downvote_advice')

    def __unicode__(self):
        return "created: {0} advice_content: {1} question_id: {2} advised_by: {3} upvote_by: {4} downvote_by: {5}".format(
            self.created, self.advice_content,
            self.question_id, self.advised_by, self.upvote_by, self.downvote_by)


# class Vote(models.Model):
#     QUESTION = 'question'
#     ADVICE = 'advice'
#     ENTITY_TYPE_CHOICES = ((QUESTION, 'question'),
#                            (ADVICE, 'advice'))
#     created = models.DateTimeField(auto_now_add=True)
#     advice = models.ForeignKey(Advices, related_name='upvotes_advices', null=True, default=None)
#     question = models.ForeignKey(Questions, related_name='upvotes_questions', null=True, default=None)
#     entity_type = models.CharField(max_length=10, choices=ENTITY_TYPE_CHOICES, blank=True, default='')
#     upvote_by_user = models.ForeignKey(User, related_name='advicesv1_upvotes', null=True, default=None,
#                                        on_delete=models.CASCADE)
#     downvote_by_user = models.ForeignKey(User, related_name='advicesv1_downvotes', null=True, default=None,
#                                          on_delete=models.CASCADE)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Stories(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    story_content = models.CharField(max_length=500)

# Create your models here.
