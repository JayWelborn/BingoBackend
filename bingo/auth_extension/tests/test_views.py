from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from auth_extension.models import UserProfile


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

        self.client.logout()

        response = self.client.get(reverse('auth_extension:login_redirect'))
        self.assertRedirects(
            response=response,
            expected_url=reverse('registration:auth_login'),
            status_code=301
        )

    def test_authenticated_user_(self):
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

    def test_authenticated_user_no_profile(self):
        """
        If a user somehow exists without a matching profile, logging in
        should create a profile associated with said user
        """

        # Create and Authenticate new user with no profile
        new_user = User.objects.get_or_create(
            username='billy',
            email='billy@bill.net'
        )[0]

        new_user.set_password('hamandjam2929!@#$')
        new_user.save()

        self.client.login(
            username='billy',
            password='hamandjam2929!@#$'
        )

        # Ensure new user logged in successfully
        self.assertIn('_auth_user_id', self.client.session)

        # Check that redirect response created profile associated with user
        response = self.client.get(
            reverse('auth_extension:login_redirect')
        )

        new_profile = UserProfile.objects.get(user=new_user)
        self.assertTrue(new_profile)
        self.assertEqual(new_profile.user, new_user)
        self.assertRedirects(
            response=response,
            expected_url=reverse(
                'auth_extension:profile_edit',
                args=[new_profile.pk]
            ),
            status_code=301
        )


class RegistrationViewTests(TestCase):
    """ Tests for Registration View

    Methods:
        test_form_valid_creates_and_authenticates_user: Calling form_valid()
            should save form with current data and log new user in.

    References:

    """

    def test_form_valid_creates_and_authenticates_user(self):
        """
        View's form_valid() method should create and authenticate new user
        """
        user_count = User.objects.count()
        
