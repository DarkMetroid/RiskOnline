from django.conf.urls.defaults import patterns, include, url
from game.views import *
from  sign_up.views import *
from views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'risk2.views.home', name='home'),
    # url(r'^risk2/', include('risk2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	(r'^sign-up/$', sign_up),
	(r'^register/$', register),
	(r'^user/(\d{1,7})$', user),
    (r'^map/(\d{1,7})$', riskmap),
    (r'^game/(\d{1,7})', game),
	(r'^$', homepage),
	
)
