from django.contrib.auth.models import User
from django.conf import settings
from xml.dom.minidom import parseString
from django.contrib.auth.backends import ModelBackend
import httplib2
import json


class JiraBackend(ModelBackend):
    """
    This is the Attlasian CROWD (JIRA) Authentication Backend for Django
    Have a nice day! Hope you will never need opening this file looking for a bug =)
    """

    def authenticate(self, username, password):
        """
        Main authentication method
        """
        jira_url = self._get_jira_config()
        if not jira_url:
            return None
        user = self._find_existing_user(username)
        resp, content = self._call_jira(username, password, jira_url)
        if resp['status'] == '200':
            if user:
                user.set_password(password)
            else:
                self._create_new_user_from_jira_response(username, password, content, jira_url)
            return user
        else:
            return None

    def _get_jira_config(self):
        """
        Returns CROWD-related project settings. Private service method.
        """
        config = getattr(settings, 'JIRA_URL', None)
        if not config:
            raise UserWarning('Jira configuration is not set in your settings.py, while authorization backend is set')
        return config

    def _find_existing_user(self, username):
        """
        Finds an existing user with provided username if one exists. Private service method.
        """
        users = User.objects.filter(username=username)
        if users.count() <= 0:
            return None
        else:
            return users[0]

    def _call_jira(self, username, password, jira_url):
        """
        Calls Jira user directory service via REST API
        """
        body = '{"username" : "%s", "password" : "%s"}' % (username, password)
        h = httplib2.Http(disable_ssl_certificate_validation=True)
        url = jira_url + "/auth/latest/session"
        resp, content = h.request(url, "POST", body=body, headers={'content-type': 'application/json'})
        return resp, content # sorry for this verbosity, but it gives a better understanding

    def _create_new_user_from_jira_response(self, username, password, content, jira_url):
        """
        Creating a new user in django auth database basing on information provided by CROWD. Private service method.
        """
        user_data = self._get_user_data(username, password, jira_url)
        if not user_data:
            email = "user@example.com"
        else:
            email = user_data['emailAddress']
        user = User.objects.create_user(username, email, password)
        user.is_active = True
        # auto-superuser goodness goes here once I figure things out
        # if 'superuser' in crowd_config and crowd_config['superuser']:
        #     user.is_superuser = crowd_config['superuser']
        #     user.is_staff = user.is_superuser
        user.save()
        return user

    def _get_user_data(self, username, password, jira_url):
        h = httplib2.Http(disable_ssl_certificate_validation=True)
        url = jira_url + "/api/latest/user?username=%s" % username
        auth = username + ':' + password
        auth = auth.encode('base64')
        resp, content = h.request(url, "GET", headers={'Authorization': 'Basic ' + auth})
        if not resp.status == 200:
            return None
        return json.loads(content)

    def _parse_crowd_response(self, content):
        """
        Returns e-mail, first and last names of user from provided CROWD response. Private service method.
        """
        dom = parseString(content)
        return {
            'email': self._get_user_parameter_from_dom_tree(dom, 'email'),
            'first_name': self._get_user_parameter_from_dom_tree(dom, 'first-name'),
            'last_name': self._get_user_parameter_from_dom_tree(dom, 'last-name'),
        }

    def _get_user_parameter_from_dom_tree(self, dom, parameter):
        """
        A small service method for dom tree parsing. Private service method.
        """
        # here I'm starting to doubt if a method that small is still a good refactoring practice. Still, no worries, eh?
        return dom.getElementsByTagName(parameter)[0].firstChild.nodeValue
