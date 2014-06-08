import sys
import os
import pytest
import datetime
from optparse import OptionParser
import site
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
python_version_number = sys.version[0:3]
site.addsitedir(os.path.join(os.path.abspath(os.path.split(__file__)[0]), '..', 've', 'lib', 'python' + python_version_number, 'site-packages'))
sys.path.append(os.path.join(os.path.abspath(os.path.split(__file__)[0]), '..'))
sys.path.append(os.path.join(os.path.abspath(os.path.split(__file__)[0]), '..', 'toptal_site'))


def main(argv):
    parser = OptionParser()
    parser.add_option('-e', '--env', type='string', dest='environment',
                      help='The environment you are working in. e.g. production')
    (options, args) = parser.parse_args()

    if options.environment:
        settings_module = 'test_site.' + options.environment + '_settings'
    else:
        settings_module = 'test_site.settings'

    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
    # Now you can import Django stuff
    import pytest
    from django import VERSION as version
    from django.conf import settings
    from django.contrib.sites.models import Site
    from django.core.mail import EmailMultiAlternatives, get_connection
    from django.template.loader import render_to_string
    import test_site.settings
    print(version)


  #TestExpenses.test_profile_view(self=None)






@pytest.mark.django_db
class TestExpenses:

    def test_profile_view(self):

        response = self.client.post(reverse('log_in_form_event'),
                                    {'success': True, 'username': 'user1', 'password': 'asdf', 'note': "password is good"})
        user = User.objects.get(username='user1')
        assert user.is_authenticated()
        print("passed")





# Need this below

if __name__ == '__main__':
  main(sys.argv[1:])
