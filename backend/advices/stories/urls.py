from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from stories import views,  comment, vote
from rest_framework_docs import urls

urlpatterns = [
    url(r'^api/postStory', views.post_story, name='stories'),
    url(r'^api/getStories/$', views.get_stories),
    url(r'^api/postComment', comment.post_comment),
    url(r'^api/getAllComments/(?P<story_id>[0-9]+)', comment.get_all_comments),
    url(r'^api/updateStoryVoteInfo', vote.update_story_vote_info)
    # url(r'^api/createAdvice', advice.create_advice)
]

#urlpatterns = format_suffix_patterns(urlpatterns)
