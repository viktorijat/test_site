from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
from account.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'toptal_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls'))',

    url(r'^home/', home, name='home'),

    url(r'^test/', test, name='test'),

    url(r'^admin/', include(admin.site.urls)),
    #media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, }),


    #static
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, }),

)
