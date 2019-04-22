from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class APIRootTestCase(APITestCase):
    """Tests for Custom API Root Class.

    Custom API Root should return a response with rest_auth urls added to my
    project urls. This includes the rest auth project URLS in the browsable API,
    to assist in debugging.

    Methods:
        test_api_root: Ensure response contains both my app urls and rest_auth
            urls.
    """

    def setUp(self):
        """
        Set some variables needed
        """
        self.url_prefix = 'http://testserver'

    def test_api_root(self):
        client = APIClient()
        response = client.get(reverse('api-root'))
        expected_additions = {
            'login': 'rest_auth:rest_login',
            'logout': 'rest_auth:rest_logout',
            'password_reset': 'rest_auth:rest_password_reset',
            'password_reset_confirm': 'rest_auth:rest_password_reset_confirm',
            'password_change': 'rest_auth:rest_password_change',
            'register': 'rest_registration:rest_register',
            'verify_email': 'rest_registration:rest_verify_email',
        }
        for key, value in expected_additions.items():
            self.assertIn(key, response.data)
            self.assertEqual(self.url_prefix + reverse(value),
                             response.data[key])
