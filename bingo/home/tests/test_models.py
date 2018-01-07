from django.test import TestCase
from django.utils import timezone

from home.models import Contact


# Create your tests here.
class ContactModelTest(TestCase):
    """Tests for Contact Model

    Methods:
        setUp: Creates sample Contact object for running tests
        test_str_method: Ensures __str__ method returns object's title

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/
    """

    def setUp(self):
        """
        Create Instance(s) for tests
        """
        Contact.objects.get_or_create(title='title',
                                      facebook='www.facebook.com',
                                      github='www.github.com',
                                      linkedin='www.linkedin.com',
                                      twitter='www.twitter.com',
                                      email='some_email@something.com')

    def test_str_method(self):
        """
        __str__ method should return contact object's title
        """
        contact = Contact.objects.latest('contact_date')
        self.assertEqual(contact.title, str(contact))
