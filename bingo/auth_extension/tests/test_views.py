from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from auth_extension.models import UserProfile

import pdb


class LoginRedirectViewTests(TestCase):
    """Tests for RedirectView

    Methods:
        setUp: create User instance for tests
        test_unauthenticated_redirect: redirect without user logged in should
            point to login page
        test_authenticated_redirect: redirect with user logged in should point
            to profile edit page

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/

    """

    def setUp(self):
        """
        Create User for testing
        """
        user = User.objects.get_or_create(
            username='jimbobtheuser',
            email='jimbob@aol.net'
        )[0]
        user.set_password('ladybug234!')
        user.save()

        self.user = User.objects.get(username='jimbobtheuser')
        self.profile = UserProfile.objects.get_or_create(user=self.user)[0]

    def test_unauthenticated_user(self):
        """
        View should redirect to login page with status code of 301
        """
        response = self.client.get(reverse('auth_extension:login_redirect'))
        self.assertRedirects(
            response=response,
            expected_url=reverse('auth_extension:login'),
            status_code=301
        )

    def test_authenticated_user(self):
        """
        View should redirect to profile edit page for authenticated user
        """
        self.client.login(
            username='jimbobtheuser',
            password='ladybug234!'
        )

        response = self.client.get(reverse(
            'auth_extension:login_redirect',
        ))

        self.assertRedirects(
            response=response,
            expected_url=reverse(
                'auth_extension:profile_edit',
                args=[self.profile.pk]
            ),
            status_code=301
        )
