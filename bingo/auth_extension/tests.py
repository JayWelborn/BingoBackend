from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.test import TestCase

# Create your tests here.
from .models import UserProfile
from .forms import RegistrationForm, ProfileForm


class UserProfileModelTests(TestCase):
    """Tests for Contact Model

    Methods:
        setUp: Creates sample UserProfile object for testing
        test_profile_links_to_user: Ensures User and UserProfile objects are
            linked as expected
        test_slugify_for_user_profile: Ensures username is correctly slugified
            when UserProfile instance is saved

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/

    """

    def setUp(self):
        """
        Create instance(s) for tests
        """
        self.test_user_one = User.objects.create(username='test one',
                                                 password='password',
                                                 email='test@test.com',)

        self.test_user_two = User.objects.create(username='test two',
                                                 password='password1',
                                                 email='test2@test.com')

        self.test_profile = UserProfile.objects.create(user=self.test_user_one)

    def test_profile_links_to_user(self):
        """
        Test to ensure UserProfile object is linked to a User upon creation
        """
        self.assertEqual(self.test_profile.user, self.test_user_one)
        self.assertEqual(self.test_user_one.profile, self.test_profile)

    def test_slugify_for_user_profile(self):
        """
        Test to ensure username slug is stored as expected when UserProfile
        instance is created
        """
        test_slug = slugify(self.test_user_one.username)
        self.assertEqual(self.test_profile.slug, test_slug)
        self.assertEqual(self.test_profile.slug, 'test-one')


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

        user = form.save()
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
            'username': 'Rick Sanchez',
            'password': 'M0rty-!5-My-53Cre7-CR|_|5|-|',
            'password_confirmation': 'M0rty-!5-My-53Cre7-CR|_|5|-|',
            'email': 'plumbusdinglebop@gmail.com',
        })
        self.assertEqual(form.helper.form_id, 'registration_form')
        self.assertEqual(form.helper.form_method, 'post')
        self.assertEqual(form.helper.form_action, '.')


class ProfileFormTests(TestCase):
    """Tests for ProfileForm

    Methods:
        test_form_has_helper: Form has helper from crispy_forms app


    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/
        * http://django-crispy-forms.readthedocs.io/en/latest/crispy_tag_forms.html

    """

    def test_form_has_helper(self):
        form = ProfileForm()
        self.assertEqual(form.helper.form_id, 'profile_form')
        self.assertEqual(form.helper.form_method, 'post')
        self.assertEqual(form.helper.form_action, '.')
