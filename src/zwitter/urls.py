from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

#the url pattern ,user is served according to requested url from views.py and template directory
urlpatterns = patterns('zwitter.views',
    url(r'^$','index'),
    url(r'^test/','test'),
    url(r'^home/','home'),
    url(r'^tweet_post/','tweet_post'),
    url(r'^register/','process_signup'),
    url(r'^login/','login_signup'),
    url(r'^logout/','logout'),
    url(r'^login_process/','login_process'),
    url(r'^admin/', include(admin.site.urls)),
)

