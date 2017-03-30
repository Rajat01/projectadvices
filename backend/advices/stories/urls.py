from django.conf.urls import url
from stories import views,  comment, vote


app_name = 'stories'
urlpatterns = [
    # Stories related urls
    url(r'^api/postStory', views.post_story, name='createstory'),
    url(r'^api/getStories/$', views.get_stories, name='getstories'),

    # Comment related urls
    url(r'^api/postComment', comment.post_comment, name='postcomment'),
    url(r'^api/getAllComments/(?P<story_id>[0-9]+)', comment.get_all_comments, name=''),

    # Vote related urls
    url(r'^api/updateStoryVoteInfo', vote.update_story_vote_info)
]

#urlpatterns = format_suffix_patterns(urlpatterns)
