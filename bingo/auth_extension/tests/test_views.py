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
            expected_url=reverse('auth_login'),
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


class ProfileRedirectViewTests(TestCase):
    """Tests for Profile Redirect View.

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
        )[0]
        self.private_profile.private = True
        self.private_profile.save()

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

        self.assertRedirects(
            response=response,
            expected_url=reverse(
                'auth_extension:profile_view',
                args=[self.public_profile.pk]
            ),
            status_code=301
        )

        # profile = response.context['profile']

        # self.assertEqual(profile.pk, self.public_profile.pk)
        # self.assertEqual(profile.user, self.public_profile.user)

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
            expected_url=reverse('auth_extension:permission_denied'),
            status_code=301
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

        self.assertRedirects(
            response=response,
            expected_url=reverse(
                'auth_extension:profile_view',
                args=[self.private_profile.pk]
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
    """Tests for ProfileView.

    Methods:
        setUp: Create profiles to view
        test_unauthenticated_redirects: unauthenticated visitors should be
            sent to login-required url.
        test_correct_template_used: View should use profile_view.html.
        test_correct_profile_in_context: response's context data should contain
            Profile matching pk sent via URL.

    References:
         * https://docs.djangoproject.com/en/1.11/topics/testing
    """

    def setUp(self):
        """
        Create profile to view in tests.
        """

        self.user = User.objects.get_or_create(
            username='profile-view-test',
            email='profile-view@gmail.com'
        )[0]
        self.user.set_password('ProfileViewTests')
        self.user.save()

        self.profile = UserProfile.objects.get_or_create(
            user=self.user,
        )[0]
        self.profile.website = 'http://www.test-profile-view.com'
        self.profile.save()

        self.viewer = User.objects.get_or_create(
            username='testviewer',
            email='testviewer@gmail.com'
        )[0]
        self.viewer.set_password('Testing123')
        self.viewer.save()

    def test_unauthenticated_redirects(self):
        """
        Attempts to view profiles by unauthenticated users should redirect to
        login-required page.
        """

        self.client.logout()

        response = self.client.get(
            reverse('auth_extension:profile_view', args=[self.profile.pk])
        )

        self.assertRedirects(
            response=response,
            expected_url='/profile/login-required/',
        )

    def test_correct_template_used(self):
        """
        View should use profile_view.html
        """

        self.client.login(
            username=self.viewer.username,
            password='Testing123'
        )

        response = self.client.get(
            reverse(
                'auth_extension:profile_view',
                args=[self.profile.pk]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='auth_extension/profile_view.html'
        )

    def test_correct_profile_in_context(self):
        """
        Assert that correct user's information was retrieved and passed in
        context.
        """

        self.client.login(
            username=self.viewer.username,
            password='Testing123'
        )

        response = self.client.get(
            reverse(
                'auth_extension:profile_view',
                args=[self.profile.pk]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context)
        self.assertIn('profile', response.context)
        self.assertEqual(response.context['profile'], self.profile)


class ProfileEditViewTests(TestCase):
    """Tests for Profile Edit View.

    Methods:
        setUp: create User, Profile, and dictionary of form data for testing.
        test_correct_template_used: View should render
            `auth_extension/profile_edit.html`.
        test_initial_form_data: Form should populate data with current user's
            profile info.
        test_view_accepts_valid_data: if form data is valid, view should not
            return any errors.
        test_existing_profile_updated: When presented valid data, view should
            update a profile if it already exists.
        test_no_duplicate_profiles: After form has been run many times
            successfuly, each User should still only have one associated
            Profile.
        test_redirect_unauthenticated_user: View should redirect
            unauthenticated users to `/profile/login-required`.

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing

    """

    def setUp(self):
        """
        Create Users, Profiles, and form data dictionary for testing.
        """

        # Create User With Profile
        user_with_profile = User.objects.get_or_create(
            username='ihaveaprofile',
            email='hasprofile@gmail.com'
        )[0]
        user_with_profile.set_password('w1thpr0F!le')
        user_with_profile.save()
        self.user_with_profile = user_with_profile

        self.assertTrue(self.user_with_profile),
        self.assertEqual(
            self.user_with_profile.username,
            'ihaveaprofile'
        )
        self.assertEqual(
            self.user_with_profile.email,
            'hasprofile@gmail.com'
        )

        # Create user without Profile
        user_without_profile = User.objects.get_or_create(
            username='ihavenoprofile',
            email='noprofile@gmail.com'
        )[0]
        user_without_profile.set_password('n0proF!le')
        user_without_profile.save()
        self.user_without_profile = user_without_profile

        self.assertTrue(self.user_without_profile),
        self.assertEqual(
            self.user_without_profile.username,
            'ihavenoprofile'
        )
        self.assertEqual(
            self.user_without_profile.email,
            'noprofile@gmail.com'
        )

        # Create Profile for first User
        first_profile = UserProfile.objects.get_or_create(
            user=self.user_with_profile,
        )[0]
        first_profile.website = 'www.example.com'
        first_profile.about_me = 'I had a profile originally'
        first_profile.save()
        self.first_profile = first_profile

        self.assertTrue(self.first_profile)
        self.assertEqual(
            self.first_profile.user,
            self.user_with_profile,
        )
        self.assertEqual(
            self.first_profile.website,
            'www.example.com'
        )
        self.assertEqual(
            self.first_profile.about_me,
            'I had a profile originally'
        )

        self.form_data = {
            'picture': None,
            'website': 'http://www.testform.com',
            'private': False,
            'about_me': 'Test Form Data'
        }

    def test_correct_template_used(self):
        """
        View should render `auth_extension/profile_edit.html`.
        """

        self.client.login(
            username='ihaveaprofile',
            password='w1thpr0F!le'
        )

        response = self.client.get(
            reverse(
                'auth_extension:profile_edit',
                args=[self.first_profile.pk])
        )

        self.assertTemplateUsed(
            response=response,
            template_name='auth_extension/profile_edit.html'
        )
        self.assertEqual(response.status_code, 200)

        self.client.logout()

    def test_initial_form_data(self):
        """
        Form's initial data should be populated with data from profile.
        """

        self.client.login(
            username='ihaveaprofile',
            password='w1thpr0F!le'
        )

        response = self.client.get(
            reverse(
                'auth_extension:profile_edit',
                args=[self.first_profile.pk])
        )

        # get initial values for form fields
        initial = response.context['form'].initial

        self.assertEqual(
            initial['website'],
            self.first_profile.website
        )
        self.assertEqual(
            initial['about_me'],
            self.first_profile.about_me
        )

    def test_view_accepts_valid_data(self):
        """
        When given valid data, form should edit Profile object associated with
        authenticated user.
        """

        self.client.login(
            username='ihaveaprofile',
            password='w1thpr0F!le'
        )

        response = self.client.post(
            reverse(
                'auth_extension:profile_edit',
                args=[self.first_profile.pk]),
            self.form_data
        )

        profile = UserProfile.objects.get(pk=self.first_profile.pk)

        self.assertEqual(
            profile.website,
            self.form_data['website'])
        self.assertEqual(
            profile.about_me,
            self.form_data['about_me'])
        self.assertEqual(response.status_code, 302)

        self.client.logout()

    def test_existing_profile_updated(self):
        """
        If user submits valid form, their profile should be updated.
        """
        self.client.login(
            username='ihaveaprofile',
            password='w1thpr0F!le'
        )

        self.form_data['website'] = 'http://www.example2.com'
        self.form_data['about_me'] = 'I have updated my profile'

        response = self.client.post(
            reverse(
                'auth_extension:profile_edit',
                args=[self.first_profile.pk]),
            self.form_data
        )

        profile = UserProfile.objects.get(pk=self.first_profile.pk)

        self.assertEqual(
            profile.website,
            self.form_data['website'])
        self.assertEqual(
            profile.about_me,
            self.form_data['about_me'])
        self.assertEqual(response.status_code, 302)

        self.client.logout()

    def test_no_duplicate_profiles(self):
        """
        Submitting data to ProfileEdit view should replace current user's
        profile data; it should not create a new profile.
        """

        self.client.login(
            username='ihaveaprofile',
            password='w1thpr0F!le'
        )

        self.form_data['website'] = 'http://www.updated.com'
        self.form_data['about_me'] = 'I have updated my profile again omg.'

        response = self.client.post(
            reverse(
                'auth_extension:profile_edit',
                args=[self.first_profile.pk]),
            self.form_data
        )

        self.assertEqual(response.status_code, 302)

        profiles = UserProfile.objects.filter(user=self.user_with_profile)

        self.assertEqual(len(profiles), 1)
        self.assertEqual(
            profiles[0].website,
            self.form_data['website']
        )

        self.client.logout()

    # def test_success_message_present(self):
    #     """
    #     Successful Posting should result in success message.
    #     """
    #     self.client.login(
    #         username='ihaveaprofile',
    #         password='w1thpr0F!le'
    #     )

    #     self.form_data['website'] = 'http://www.updatedyetagain.com'
    #     self.form_data['about_me'] = 'Seriously. Another Test'

    #     response = self.client.post(
    #         reverse(
    #             'auth_extension:profile_edit',
    #             args=[self.first_profile.pk]),
    #         self.form_data
    #     )

    #     message = list(response.context['messages'])[0]
    #     self.assertEqual(message.tags, "success")
    #     self.assertTrue("success text" in message.message)

    def test_redirect_unauthenticated_user(self):
        """
        Unauthenticated user should not be allowed to view ProfileEdit View.
        """

        self.client.logout()

        response = self.client.get(reverse(
            'auth_extension:profile_edit',
            args=[self.first_profile.pk]
        ))

        self.assertRedirects(
            response=response,
            expected_url=reverse('auth_extension:unauthorized'),
            status_code=302
        )


class ProfileListViewTests(TestCase):
    """Tests for Profile List View.

    Methods:
        setUp: Create users and profiles for testing
        test_unauthenticated_visitor: Private profiles should not be visible to
            unauthenticated visitors.
        test_authenticated_visitor: Private profiles should be visible to
            authenticated visitors.

    References:

    """

    def setUp(self):
        """
        Create private and public profiles for testing
        """

        self.public_profiles = []
        self.private_profiles = []

        for i in range(4):
            # Add private profile to list
            private_user = User.objects.get_or_create(
                username='private{}'.format(i),
                email='private{}@gmail.com'.format(i)
            )[0]
            private_user.set_password('password{}'.format(i))
            private_profile = UserProfile.objects.get_or_create(
                user=private_user,
            )[0]
            private_profile.private = True
            private_profile.save()
            private_user.profile = private_profile
            private_user.save()
            self.private_profiles.append(private_profile)

            # Add public profile to list
            public_user = User.objects.get_or_create(
                username='public{}'.format(i),
                email='public{}@gmail.com'.format(i)
            )[0]
            public_user.set_password('password{}'.format(i))
            public_user.save()
            public_profile = UserProfile.objects.get_or_create(
                user=public_user,
                private=False
            )[0]
            public_profile.save()
            self.public_profiles.append(public_profile)

    def test_unauthenticated_visitor(self):
        """
        Unauthenticated visitors should not see private profiles.
        """
        self.client.logout()
        response = self.client.get(reverse('auth_extension:profile_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('profiles', response.context)

        # Assert public profiles are in context
        for profile in self.public_profiles:
            self.assertIn(profile, response.context['profiles'])

        # Assert private profiles aren't in context
        for profile in self.private_profiles:
            self.assertNotIn(profile, response.context['profiles'])

    def test_authenticated_visotor(self):
        """
        Authenticated visitors should see all profiles.
        """
        self.client.login(
            username='private0',
            password='password0'
        )
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(reverse('auth_extension:profile_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('profiles', response.context)

        # Assert all profiles are in context
        for profile in self.private_profiles + self.public_profiles:
            self.assertIn(profile, response.context['profiles'])


class UnauthorizedTests(TestCase):
    """Tests for Unauthorized Template View

    Methods:
        test_template_used: test correct template is rendered.

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing

    """

    def test_template_used(self):
        response = self.client.get(
            reverse('auth_extension:unauthorized')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='auth_extension/login_required.html'
        )


class PermissionDeniedTests(TestCase):
    """Tests for Permission Denied Template View

    Methods:
        test_template_used: test correct template is rendered.

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing

    """

    def test_template_used(self):
        response = self.client.get(
            reverse('auth_extension:permission_denied')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='auth_extension/permission_denied.html'
        )
