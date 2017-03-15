from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User



class Story(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    story = models.CharField(max_length=1000, blank=True, default='')
    created_by = models.ForeignKey(User, related_name='stories', null=True, default=None)
    upvoted_by = models.ManyToManyField(User, default=None, related_name='upvotes')
    downvoted_by = models.ManyToManyField(User, default=None, related_name='downvotes')
    is_anonymously_posted = models.BooleanField(default=False)

    def __unicode__(self):
        return 'created: {0}, story: {1}, created_by: {2} upvoted_by: {3}' \
               'downvoted_by: {4}, is_anonymously_posted: {5}'.format(self.created, self.story,
                                                                      self.created_by, self.upvoted_by,
                                                                      self.downvoted_by, self.is_anonymously_posted)



class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=500, blank=True, default='')
    story = models.ForeignKey(Story, related_name='storycomments', null=True, default=None)
    commented_by = models.ForeignKey(User, related_name='comments', null=True, default=None)

    def __unicode__(self):
        return 'created: {0}, comment {1}, story: {2}, commented_by: {3}'.format(self.created, self.comment,
                                                                                 self.story, self.commented_by)


# Create your models here.
