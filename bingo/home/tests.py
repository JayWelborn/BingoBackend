from django.test import TestCase
from django.utils import timezone

from .models import Contact

# Create your tests here.
class ContactModelTest(TestCase):
    """
    Tests for Contact Model
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
                                      email='some_email@something.com',
                                      contact_date=timezone.now())

    def test_str_method(self):
        """
        __str__ method should return contact object's title
        """
        contact = Contact.objects.latest('contact_date')
        self.assertEqual(contact.title, str(contact))
