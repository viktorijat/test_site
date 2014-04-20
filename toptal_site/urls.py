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

    url(r'^register_form_event/', register_form_event, name='register_form_event'),

    url(r'^log_in_form_event/', log_in_form_event, name='log_in_form_event'),

    url(r'^logout_user/', logout_user, name='logout_user'),

    url(r'^profile/', profile, name='profile'),


    url(r'^admin/', include(admin.site.urls)),
    #media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, }),


    url(r'^expense_added/', expense_added, name='expense_added'),


    #static
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, }),

)
