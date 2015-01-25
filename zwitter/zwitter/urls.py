from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('zwitter.views',
    url(r'^$','index'),
    url(r'^register/','process_signup'),
    url(r'^admin/', include(admin.site.urls)),
)

