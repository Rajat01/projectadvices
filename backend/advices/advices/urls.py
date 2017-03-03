"""advices URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from advicesv1 import views, api
from rest_framework.authtoken import views as auth_token_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/getQuestionList', views.get_question_list),
    url(r'^api/createQuestion', views.create_question),
    url(r'^api/createAdvice', views.create_advice),
    url(r'^api/getAllAdvices/(?P<pk>[0-9]+)', views.get_all_advices),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^api/deleteAdvice/(?P<pk>[0-9]+)', views.delete_advice_question),
    url(r'^api/updateQuestionUpvotes', views.update_question_upvote_count),
    url(r'^api/deleteQuestion/(?P<pk>[0-9]+)', views.delete_question),
    url(r'^api/auth/signup', api.sign_up),
    url(r'api/auth/login', api.login_user),
    url(r'api/auth/logout', api.logout_user)
]


urlpatterns += [
    url(r'^api/token-auth/', auth_token_views.obtain_auth_token)
]


urlpatterns = format_suffix_patterns(urlpatterns)
