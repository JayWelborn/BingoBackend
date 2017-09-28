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
        test_url_uses_correct_template: GET request to view returns status code
             200 and uses the correct template.
        test_view_rejects_invalid_username: View should reject invalid username
            and render appropriate error message.
        test_view_rejects_invalid_email: View should reject invalid email and
            render appropriate error message.
        test_view_rejects_invalid_password: View should reject invalid password
            and render appropriate error message.
        test_view_rejects_common_password: View should reject Passwords that
            commonly cause security problems and render appropriate error
            message
        test_view_accepts_valid_data_and_redirects: View should accept valid
            data, create new User, and redirect to LoginRedirectView.

    References:
        * http://www.obeythetestinggoat.com/testing-django-class-based-generic-views.html

    """

    def test_url_uses_correct_template(self):
        """
        GET requested routed to this view should return a status code of 200
        and use registration/registration_form.html for rendering.
        """
        response = self.client.get(reverse('registration_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'registration/registration_form.html'
        )

    def test_view_rejects_invalid_username(self):
        """
        Submitting invalid username should result in form error, and not
        create a new user.
        """
        count_users = User.objects.count()

        # test invalid username
        post_data = {
            'username': 'Invalid Username',
            'email': 'validemail@gmail.com',
            'password': 'thisisavalidone123',
            'password_confirmation': 'thisisavalidone123'
        }

        response = self.client.post(
            reverse('registration_register'),
            post_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'errorlist')
        self.assertContains(response, 'Enter a valid username.')
        self.assertEqual(count_users, User.objects.count())

    def test_view_rejects_invalid_email(self):
        """
        View should reject invalid email and render template with appropriate
        error message.
        """

        user_count = User.objects.count()

        post_data = {
            'username': 'Invalid Username',
            'email': 'invalidemail',
            'password': 'thisisavalidone123',
            'password_confirmation': 'thisisavalidone123'
        }

        response = self.client.post(
            reverse('registration_register'),
            post_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'errorlist')
        self.assertContains(response, 'Enter a valid email address.')
        self.assertEqual(user_count, User.objects.count())

    def test_view_rejects_mismatched_password(self):
        """
        View should reject invalid password and render template with
        appropriate error message.
        """
        user_count = User.objects.count()

        post_data = {
            'username': 'validusername',
            'email': 'validemail@gmail.com',
            'password': 'thisisavalidone123',
            'password_confirmation': 'thisisavalidone1234'
        }

        response = self.client.post(
            reverse('registration_register'),
            post_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'errorlist')
        self.assertContains(response, 'Passwords entered do not match.')
        self.assertEqual(user_count, User.objects.count())

    def test_view_rejects_common_password(self):
        """
        View rejects common password and renders appropriate error code
        """
        user_count = User.objects.count()

        post_data = {
            'username': 'validusername',
            'email': 'validemail@gmail.com',
            'password': 'password',
            'password_confirmation': 'password'
        }

        response = self.client.post(
            reverse('registration_register'),
            post_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'errorlist')
        self.assertContains(response, 'This password is too common.')
        self.assertEqual(user_count, User.objects.count())

    def test_view_accepts_valid_data_and_redirects(self):
        """
        View should accept valid POST data, create User object, and redirect
        through LoginRedirectView after authenticating the user.
        """
        user_count = User.objects.count()

        post_data = {
            'username': 'validusername',
            'email': 'validemail@gmail.com',
            'password': 'validone1234',
            'password_confirmation': 'validone1234'
        }

        response = self.client.post(
            reverse('registration_register'),
            post_data
        )

        user = User.objects.get(username='validusername')

        self.assertEqual(user_count + 1, User.objects.count())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user)
        self.assertRedirects(
            response=response,
            expected_url=reverse(
                'auth_extension:profile_edit',
                args=[user.profile.pk]),
            status_code=302
        )


class ProfileViewTests(TestCase):
    """Tests for Profile View.

    Methods:
        setUp: Create public and profiles for tests.
        test_request_from_unauthenticated_visitor: Requests from
            unauthenticated visitors should be re-routed.
        test_request_for_public_profile: Requests for public profile should
            display that profile if visitor is authenticated.
        test_request_for_private_profile_from_public: Requests for private 
            profile should be denied.
        test_request_for_private_from_private: Requests from private profiles
            to view their own details should be allowed.

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/tools/#django.test.Client.get

    """

    def setUp(self):
        """
        Create public and private profiles.
        """

        # public profile
        public_user = User.objects.get_or_create(
            username='public_user',
            email='public@gmail.com'
        )[0]
        public_user.set_password('publicuserp@55word')
        public_user.save()
        self.public_profile = UserProfile.objects.get_or_create(
            user=public_user
        )[0]

        # private profile
        private_user = User.objects.get_or_create(
            username='private_user',
            email='private@gmail.com'
        )[0]
        private_user.set_password('privateuserp@55word')
        private_user.save()
        self.private_profile = UserProfile.objects.get_or_create(
            user=private_user,
            private=True
        )[0]

        self.assertFalse(self.public_profile.private)
        self.assertTrue(self.private_profile.private)

    def test_request_from_unauthenticated_visitor(self):
        """
        Unauthenticated users should be redirected to LoginRequired.
        """

        self.client.logout()

        response = self.client.get(
            reverse(
                'auth_extension:profile',
                args=[self.public_profile.pk]
            ),
            follow=True
        )

        self.assertRedirects(
            response=response,
            expected_url=reverse('auth_extension:unauthorized'),
        )

    def test_request_for_public_profile(self):
        """
        Requesting public profile should return response of 200 and render page
        for all authenticated users.
        """

        self.client.login(
            username='public_user',
            password='publicuserp@55word'
        )
        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.get(
            reverse(
                'auth_extension:profile',
                args=[self.public_profile.pk]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('profile', response.context)

        profile = response.context['profile']

        self.assertEqual(profile.pk, self.public_profile.pk)
        self.assertEqual(profile.user, self.public_profile.user)

    def test_request_for_private_profile_from_public(self):
        """
        Requests for private profiles should be denied and redirected to
        PermissionDenied.
        """

        self.client.login(
            username='public_user',
            password='publicuserp@55word'
        )
        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.get(
            reverse(
                'auth_extension:profile',
                args=[self.private_profile.pk]
            )
        )

        self.assertRedirects(
            response=response,
            expected_url=reverse('auth_extension:permission_denied')
        )

    def test_request_for_private_from_self(self):
        """
        Users with Private Profiles should be able to view their own profiles.
        """

        self.client.logout()
        self.client.login(
            username='private_user',
            password='privateuserp@55word'
        )
        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.get(
            reverse(
                'auth_extension:profile',
                args=[self.private_profile.pk]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('profile', response.context)

        profile = response.context['profile']

        self.assertEqual(profile.pk, self.private_profile.pk)
        self.assertEqual(profile.user, self.private_profile.user)
