from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

#the url pattern ,user is served according to requested url from views.py and template directory
urlpatterns = patterns('zwitter.views',
    url(r'^$','index'),
    url(r'^register/','process_signup'),
    url(r'^admin/', include(admin.site.urls)),
)

