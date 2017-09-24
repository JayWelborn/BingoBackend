from django import forms
from django.contrib.auth.models import User
from django.test import TestCase

from auth_extension.forms import RegistrationForm, ProfileEditForm
from auth_extension.models import UserProfile


class RegistrationFormTests(TestCase):
    """Tests for Registration Form

    Methods:
        test_form_accepts_valid_data: Form accepts valid form data, and saves
            UserProfile and User objets linked appropriately
        test_form_rejects_invalid_username: Form rejects username with invalid
            character
        test_form_rejects_mismatched_password_confirmation: Form rejects
            mismatched entries for password and password_confirmation
        test_save_method_links_profile_to_user: UserProfile is linked
            to User as expected
        test_new_form_has_helper_with_appropriate_attributes: Form has helper
            from crispy_forms app

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/
        * https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#the-save-method
        * http://test-driven-django-development.readthedocs.io/en/latest/05-forms.html4
        * http://django-crispy-forms.readthedocs.io/en/latest/crispy_tag_forms.html

    """

    def test_form_accepts_valid_data(self):
        """
        Form should accept valid data
        """
        form = RegistrationForm({
            'username': 'RickSanchez',
            'password': 'M0rty-!5-My-53Cre7-CR|_|5|-|',
            'password_confirmation': 'M0rty-!5-My-53Cre7-CR|_|5|-|',
            'email': 'plumbusdinglebop@gmail.com',
        })

        form.save()

        user = User.objects.get(username='RickSanchez')

        self.assertTrue(user)
        self.assertTrue(user.password)
        self.assertEqual(user.username, 'RickSanchez')
        self.assertEqual(user.email, 'plumbusdinglebop@gmail.com')

    def test_form_rejects_invalid_username(self):
        """
        Form should reject invalid username
        """
        form = RegistrationForm({
            'username': 'Rick Sanchez',
            'password': 'M0rty-!5-My-53Cre7-CR|_|5|-|',
            'password_confirmation': 'M0rty-!5-My-53Cre7-CR|_|5|-|',
            'email': 'plumbusdinglebop@gmail.com',
        })
        self.assertFalse(form.is_valid())

    def test_form_rejects_mismatched_password_confirmation(self):
        """
        Form should reject common passwords
        """
        form = RegistrationForm({
            'username': 'RickSanchez',
            'password': 'password',
            'password_confirmation': 'password2',
            'email': 'plumbusdinglebop@gmail.com',
        })
        self.assertRaises(forms.ValidationError, form.save)

    def test_new_form_has_helper_with_appropriate_attributes(self):
        """
        Form should have form.helper with form_id, form_method, and form_action
        attributes
        """
        form = RegistrationForm({
            'username': 'RickSanchez',
            'password': 'M0rty-!5-My-53Cre7-CR|_|5|-|',
            'password_confirmation': 'M0rty-!5-My-53Cre7-CR|_|5|-|',
            'email': 'plumbusdinglebop@gmail.com',
        })
        self.assertEqual(form.helper.form_id, 'registration_form')
        self.assertEqual(form.helper.form_method, 'post')
        self.assertEqual(form.helper.form_action, '.')

    def test_valid_form_creates_profile(self):
        """
        Calling form.save() should create and instance of UserProfile linked
        to the new User.
        """

        # create form instance
        form = RegistrationForm({
            'username': 'RickSanchez',
            'password': 'M0rty-!5-My-53Cre7-CR|_|5|-|',
            'password_confirmation': 'M0rty-!5-My-53Cre7-CR|_|5|-|',
            'email': 'plumbusdinglebop@gmail.com',
        })
        self.assertTrue(form.is_valid())
        form.save()

        # retrive user and profile and verify that they exist
        user = User.objects.get(username='RickSanchez')
        profile = UserProfile.objects.get(user=user)
        self.assertTrue(user)
        self.assertTrue(profile)

        # verify that profile matches user
        self.assertEqual(profile.user, user)


class ProfileEditFormTests(TestCase):
    """Tests for ProfileEditForm

    Methods:
        setUp: Create test user for testing form.save()
        test_form_has_helper: Form has helper from crispy_forms app
        test_form_accepts_valid_data: Form should accept valid values for
            each field and form.is_valid() should return True
        test_form_saves_new_profile: Form should save new profile if one
            doesn't already exist

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/
        * http://django-crispy-forms.readthedocs.io/en/latest/crispy_tag_forms.html

    """
    def setUp(self):
        """
        Create user for testing form.save() method.
        """
        self.user = User.objects.get_or_create(
            username='RickSanchez',
            email='plumbusdinglebop@gmail.com'
        )[0]
        self.user.set_password('M0rty-!5-My-53Cre7-CR|_|5|-|')
        self.user.save()

    def test_form_has_helper(self):
        """
        Form has helper with appropriate attributes
        """
        form = ProfileEditForm()
        self.assertEqual(form.helper.form_id, 'profile_form')
        self.assertEqual(form.helper.form_method, 'post')
        self.assertEqual(form.helper.form_action, '.')

    def test_form_accepts_valid_data(self):
        """
        Calling form.is_valid() returns true when form is presented valid data.
        """
        form = ProfileEditForm({
            'picture': None,
            'website': 'www.google.com',
            'private': False,
            'about_me': 'This is my bio. It is very short'
        })

        self.assertTrue(form.is_valid())

    def test_form_saves_new_profile(self):
        """
        Calling form.save() with pk of user without associated profile should
        create new profile associated with that user.
        """
        pk = self.user.pk

        form = ProfileEditForm({
            'picture': None,
            'website': 'www.google.com',
            'private': False,
            'about_me': 'This is my bio. It is very short'
        })

        form.save(pk)

        new_profile = UserProfile.objects.get(user=self.user)

        self.assertTrue(new_profile)
        self.assertEqual(new_profile.user, self.user)
        self.assertEqual(new_profile, self.user.profile)

    def test_form_updates_existing_profile(self):
        """
        Calling form.save() with pk of user already having profile should
        update said profile.
        """

        pk = self.user.pk
        form = ProfileEditForm({
            'picture': None,
            'website': 'www.google.com',
            'private': False,
            'about_me': 'This is my bio. It is very short.'
        })
        new_profile = UserProfile.objects.get_or_create(
            user=self.user,
            picture=None,
            website='www.youtube.com',
            private=True,
            about_me='I don\'t have a bio yet'
        )[0]
        new_profile.save()

        self.assertTrue(new_profile)
        self.assertEqual(new_profile.website, 'www.youtube.com')
        self.assertTrue(new_profile.private)
        self.assertEqual(new_profile.about_me, 'I don\'t have a bio yet')

        form.save(pk)

        profile = UserProfile.objects.get(user=self.user)
        self.assertTrue(profile)
        self.assertEqual(profile, self.user.profile)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.website, 'http://www.google.com')
        self.assertFalse(profile.private)
        self.assertEqual(profile.about_me, 'This is my bio. It is very short.')
