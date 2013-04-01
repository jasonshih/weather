from django.conf.urls import patterns, include, url
from weather.apps.compare.views import test, data


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', test), # Home page
	url(r'^data/$', data), # AJAX page

    # Examples:
    # url(r'^$', 'weather.views.home', name='home'),
    # url(r'^weather/', include('weather.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)
