from __future__ import unicode_literals

from django.db import models






class Questions(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=1000, blank=True, default='')
    up_votes = models.IntegerField(blank=True, default=0)

    def __unicode__(self):
        return "created: {0} question: {1} up_votes: {2}".format(self.created, self.question, self.up_votes)




class Advices(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    advice_content = models.CharField(max_length=1000, blank=True, default='')
    question = models.ForeignKey(Questions)

    def __unicode__(self):
        return "created: {0} advice_content: {1} question: {2}".format(self.created, self.advice_content,
                                                                       self.question_id)




class Stories(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    story_content = models.CharField(max_length=500)


# Create your models here.

