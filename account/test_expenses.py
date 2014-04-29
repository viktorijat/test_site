import pytest
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
#import toptal_site.settings
from django.conf import settings

settings.configure(DEBUG=True)

@pytest.mark.django_db
class TestExpenses:

    def test_profile_view(self):

        response = self.client.post(reverse('log_in_form_event'),
                                    {'success': True, 'username': 'user1', 'password': 'asdf', 'note': "password is good"})

        user = User.objects.get(username='user1')

        assert user.is_authenticated()
