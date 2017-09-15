# django imports
from django.core import mail
from django.test import TestCase

# relative imports
from home.forms import ContactForm


class TestEmailForm(TestCase):
    """Tests for email form

    Methods:
        setUp: Create form instances for testing. One CC'd, the other not.
        test_contents_of_form: Form objects should have expected data
        test_send_email_sends_correctly: EmailMessage object should be created
            and returned. The subject, to, body, and cc should match expected
            values based on contents of the ContactForm.

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/
        * https://djangosnippets.org/snippets/10466/

    """

    def setUp(self):
        """
        Create instances of ContactForm for testing. One with CC box marked
        `True`, the other `False`.
        """

        cc_data = {
            'name': 'User',
            'email': 'useremail@textiles.com',
            'subject': 'cc_subject',
            'message': 'Hello. I hope you are having a great day',
            'cc_myself': True,
        }

        no_cc_data = {
            'name': 'User2',
            'email': 'user2email@textiles.com',
            'subject': 'no_cc_subject',
            'message': 'Hello. I hope you are having a great day',
            'cc_myself': False,
        }

        self.cc_form = ContactForm(
            cc_data, initial=cc_data
        )

        self.no_cc_form = ContactForm(
            no_cc_data, initial=no_cc_data
        )

    def test_contents_of_form(self):
        """
        Form instance was created properly with expected attributes
        """

        message = 'Hello. I hope you are having a great day'

        cc_data = self.cc_form.data
        no_cc_data = self.no_cc_form.data

        # cc_form has correct attributes
        self.assertEqual(cc_data['name'], 'User')
        self.assertEqual(cc_data['email'], 'useremail@textiles.com')
        self.assertEqual(cc_data['subject'], 'cc_subject')
        self.assertEqual(cc_data['message'], message)

        # no_cc_form has correct attributes
        self.assertEqual(no_cc_data['name'], 'User2')
        self.assertEqual(no_cc_data['email'], 'user2email@textiles.com')
        self.assertEqual(no_cc_data['subject'], 'no_cc_subject')
        self.assertEqual(no_cc_data['message'], message)

    def test_send_email_sends_correctly(self):
        """
        Form's `send email` method sends email
        """

        cc_message = self.cc_form.send_email()
        self.assertEqual(len(mail.outbox))
