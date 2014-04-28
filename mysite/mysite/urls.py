from django.conf.urls import patterns, include, url
from sliceva import views

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.login),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),

    url(r'^listdevice/$', views.listdevice),
    url(r'^adddevice/$', views.adddevice),
    url(r'^updatedevice-(?P<id>\d+)/$', views.updatedevice),
    url(r'^deletedevice-(?P<id>\d+)/$', views.deletedevice),

    url(r'^listuser/$', views.listuser),
    url(r'^adduser/$', views.adduser),
    url(r'^updateuser-(?P<id>\d+)/$', views.updateuser),
    url(r'^deleteuser-(?P<id>\d+)/$', views.deleteuser),

    url(r'^device-(?P<id>\d+)/$', views.device),
    url(r'^scan/$', views.scan),
#    url(r'^device/', 'sliceva.views.device'),
#    url(r'^single/', 'sliceva.views.single'),
#    url(r'^group/', 'sliceva.views.group'),
)
