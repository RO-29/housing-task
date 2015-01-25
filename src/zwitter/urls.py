from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

#the url pattern ,user is served according to requested url from views.py and template directory
urlpatterns = patterns('zwitter.views',
    url(r'^$','index'),
    url(r'^me/','profile'),
    url(r'^follow/','follow'),
    url(r'^unfollow/','unfollow'),
    url(r'^user/(?P<handle>\w+)','user_profile'),
    url(r'^(?P<handle>\w+)/followers/','followers_render'),
    url(r'^(?P<handle>\w+)/following','following_render'),
    url(r'^me_tweets/','get_tweets_me'),
    url(r'^list/','list_'),
    url(r'^other_user/','other_user'),
    url(r'^timeline_tweets/','get_tweets_timeline'),
    url(r'^test/','test'),
    url(r'^home/','home'),
    url(r'^tweet_post/','tweet_post'),
    url(r'^register/','process_signup'),
    url(r'^login/','login_signup'),
    url(r'^logout/','logout'),
    url(r'^login_process/','login_process'),
    url(r'^admin/', include(admin.site.urls)),
)

