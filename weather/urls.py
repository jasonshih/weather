from django.conf.urls import patterns, include, url
from weather.apps.compare.views import test, data
from django.conf import settings


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

# Code below is a stopgap for Gunicorn to serve static files until Amazon S3 can be integrated; remove ASAP
if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

