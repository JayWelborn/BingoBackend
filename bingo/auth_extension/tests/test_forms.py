from django import forms
from django.test import TestCase

from auth_extension.forms import RegistrationForm, ProfileForm


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