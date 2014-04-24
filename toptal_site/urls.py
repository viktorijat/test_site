from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
from account.views import *

from django.views.decorators.csrf import csrf_exempt


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'toptal_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls'))',

    url(r'^$', home, name='home'),
    url(r'^register_form_event/', register_form_event, name='register_form_event'),
    url(r'^log_in_form_event/', log_in_form_event, name='log_in_form_event'),
    url(r'^logout_user/', logout_user, name='logout_user'),

    url(r'^profile/', profile, name='profile'),


    url(r'^add_new_expense_url/', add_new_expense_url, name='add_new_expense_url'),
    url(r'^add_new_expense/', add_new_expense, name='add_new_expense'),
    url(r'^go_back_url/', go_back_url, name='go_back_url'),

    url(r'^details/', details, name='details'),

#    url(r'^detail_view/', DetailView.as_view(), {'template_name': 'detail_view.html'}, name='detail_view'),
    url(r'^detail_view/', detail_view, name='detail_view'),

    url(r'^expense_added/', expense_added, name='expense_added'),
    url(r'^delete_expense/', delete_expense, name='delete_expense'),
    url(r'^edit_expense/', edit_expense, name='edit_expense'),
    url(r'^calculate_day/', calculate_day, name='calculate_day'),
    url(r'^calculate_this_week/', calculate_this_week, name='calculate_this_week'),



    url(r'^admin/', include(admin.site.urls)),
    #media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, }),

    #static
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, }),

)
