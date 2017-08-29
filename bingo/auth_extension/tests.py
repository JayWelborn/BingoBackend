from django.test import TestCase
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your tests here.
from .models import UserProfile

class UserProfileModelTests(TestCase):
    """Tests for Contact Model

    Methods:
        setUp: Creates sample UserProfile object for testing
        test_profile_links_to_user: Ensures User and UserProfile objects are
            linked as expected
        test_slugify_for_user_profile: Ensures username is correctly slugified
            when UserProfile instance is saved
        

    References:
        * TODO-- link to Django docs testing url
    """

    def setUp(self):
        """
        Create instance(s) for tests
        """
        User.objects.create(username='test',
                            password='password',
                            email='test@test.com',)

        User.objects.create(username='test again',
                            password='password1',
                            email='test2@test.com')

        test_user = User.objects.get(username='test')

        UserProfile.objects.create(user=test_user)

    def test_profile_links_to_user(self):
        """
        Test to ensure UserProfile object is linked to a User upon creation
        """
        test_profile = UserProfile.objects.get(pk=1)
        test_user = User.objects.get(pk=1)
        self.assertEqual(test_profile.user, test_user)

    def test_slugify_for_user_profile(self):
        """
        Test to ensure username slug is stored as expected when UserProfile
        instance is created
        """
        test_user = User.objects.get(username='test again')
        test_profile = UserProfile.objects.create(user=test_user)

        self.assertEqual(test_profile.slug, slugify(test_user.username))
        self.assertEqual(test_profile.slug, 'test-again')
