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
        test_send_cc_email_sends_correctly: EmailMessage object should be created
            and returned. The subject, to, body, and cc should match expected
            values based on contents of the ContactForm.
        test_no_cc_email_sends_correctly: Same as above, but there should be no
            cc recipients

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

    def test_send_cc_email_sends_correctly(self):
        """
        Form's `send email` method sends email with cc
        """

        # send email and check objects for equality
        cc_message = self.cc_form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(cc_message, message)

        # ensure sent email has expected values
        cc_recipients = ['jesse.welborn@gmail.com', 'useremail@textiles.com']
        body = 'Sender Name: User \nSender Email: useremail@textiles.com\n\n'
        body += ' Hello. I hope you are having a great day.'

        self.assertEqual(message.recipients(), cc_recipients)
        self.assertEqual(message.to, ['jesse.welborn@gmail.com'])
        self.assertEqual(message.subject, 'cc_subject')
        self.assertEqual(message.cc, ['useremail@textiles.com'])

    def test_send_email_sends_correctly(self):
        """
        Form's `send email` method words correctly without cc
        """
        # send email and check objects for equality
        no_cc_message = self.no_cc_form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message, no_cc_message)

        # ensure sent email has expected values
        recipients = ['jesse.welborn@gmail.com']
        body = 'Sender Name: User2 \nSender Email: user2email@textiles.com\n\n'
        body += ' Hello. I hope you are having a great day.'

        self.assertEqual(message.recipients(), recipients)
        self.assertEqual(message.to, ['jesse.welborn@gmail.com'])
        self.assertEqual(message.subject, 'no_cc_subject')
        self.assertFalse(message.cc)
