from django.conf.urls import url
import advice
import views
import vote

#app_name = 'advicesv1'
urlpatterns = [
    # Question related urls
    url(r'^api/getQuestionList', views.get_question_list),
    url(r'^api/createQuestion', views.create_question),
    url(r'^api/deleteQuestion/(?P<pk>[0-9]+)', views.delete_question),
    url(r'api/editQuestion', views.update_question),

    # Advice related urls
    url(r'^api/createAdvice', advice.create_advice),
    url(r'^api/getAllAdvices/(?P<question_id>[0-9]+)', advice.get_all_advices),
    url(r'^api/deleteAdvice/(?P<pk>[0-9]+)', advice.delete_advice_question),
    url(r'api/editAdvice', advice.update_advice),

    # Vote related urls
    url(r'^api/updateQuestionUpvotesInfo', vote.update_question_upvote_info),
    url(r'api/updateAdviceVoteInfo', vote.update_advice_vote_info),
]
