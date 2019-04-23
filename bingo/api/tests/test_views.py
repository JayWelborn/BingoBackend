from copy import copy

from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from api.views import EmailFormView


class EmailFormViewTests(APITestCase):
    """Tests for Email Form View

    Methods:
        test_post: Email should be sent on POST with valid data. Invalid Data
            should result in 400 Bad Request
    """

    def test_post(self):
        """
        Send Email view should successfully send email on POST with valid data.
        Invalid data should return 400 Bad Request
        """
        valid_data = {
            "name": "Soumebody",
            "email": "jay@jaywelborn.com",
            "subject": "Running Tests Again",
            "body": "This is a test email from testing a Django App",
        }
        invalid_data = copy(valid_data)
        invalid_data['email'] = 'invalid_email'

        view = EmailFormView.as_view()

        factory = APIRequestFactory()
        valid_request = factory.post(reverse('contact'), valid_data)
        response = view(valid_request)
        self.assertEqual(response.status_code, 201)

        invalid_request = factory.post(reverse('contact'), invalid_data)
        response = view(invalid_request)
        self.assertEqual(response.status_code, 400)
