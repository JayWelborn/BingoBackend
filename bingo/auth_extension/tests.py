from django.test import TestCase
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your tests here.
from .models import UserProfile
from .forms import RegistrationForm


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
        test_form_accepts_valid_data: Form accepts valid form data
        test_form_rejects_empty_fields: Form raises appropriat errors on
            empty fields
        test_save_method_creates_profile_object: UserProfile object is created
            when form.save() is called
        test_save_method_links_profile_to_user: UserProfile is linked
            to User as expected

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/
        * https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#the-save-method
        * http://test-driven-django-development.readthedocs.io/en/latest/05-forms.html

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
