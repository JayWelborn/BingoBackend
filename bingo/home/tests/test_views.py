# python imports
from datetime import timedelta

# django imports
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# app imports
from cards.models import BingoCard
from home.models import Contact

# relative imports
from .helpers import create_user, create_card


# Start test classes
class IndexViewTests(TestCase):
    """Tests for Index View.

    Methods:
        setUp: Creates public and private users, and public and private
            BingoCards to test
        test_response_code: View should respond with code 200 (all good, baby)
        test_context_object_name: Context Object Name should be `card_list`
        test_authenticated_visitor: An authenticated User should be able to see
            both public and private cards
        test_unauthenticated_visitor: An unauthenticated visitor should be able
            to see only public cards with public creators

    References:

        * https://docs.djangoproject.com/en/1.11/topics/testing/
        * https://docs.djangoproject.com/en/1.11/topics/testing/tools/

    """

    def setUp(self):
        """
        Create private and public users that each have private and public
        Cards.
        """

        # create public and private users
        self.private_user = create_user('private', 'fleerdygort', True)
        self.public_user = create_user('public', 'foobar', False)

        self.users = [self.private_user, self.public_user]

        # create private cards for each user
        self.cards = []
        for user in self.users:
            title1 = user.username
            new_card = create_card(title1, user, True)
            self.cards.append(new_card)

        # create public cards for each user
        for user in self.users:
            title = user.username
            new_card = create_card(title, user, False)
            self.cards.append(new_card)

    def test_response_code(self):
        """
        Response code should be 200
        """
        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)

    def test_context_object_name(self):
        """
        Context Object should be called `card_list`
        """
        response = self.client.get(reverse('home:index'))
        self.assertIn('card_list', response.context)

    def test_authenticated_visitor(self):
        """
        Authenticated visitor should receive 5 most recent cards, including
        private cards. Should receive all if less than 5 in DB.
        """
        self.client.login(username='private', password='fleerdygort')
        response = self.client.get(reverse('home:index'))

        # there should be 4 cards as we created 4 cards earlier
        self.assertEqual(len(response.context['card_list']), 4)

        # ensure Queryset contains correct cards
        cards = BingoCard.objects.distinct()
        qs = response.context['card_list']

        for card in cards:
            self.assertIn(card, qs)

    def test_unauthenticated_visitor(self):
        """
        Unauthenticated visitor should receive Queryset containing only public
        cards. In this case, should be 2 cards.
        """
        response = self.client.get(reverse('home:index'))

        # there should only be 2 cards in context['card_list']
        self.assertEqual(len(response.context['card_list']), 2)

        # ensure Queryset contains correct cards
        cards = BingoCard.objects.filter(private=False)
        qs = response.context['card_list']

        for card in cards:
            self.assertIn(card, qs)


class ContactViewTests(TestCase):
    """Tests for Contact View.

    Methods:
        setUp: Creates 2 contact objects, and one User for testing
        test_response_code: View should respond with code 200 (all good, baby)
        test_contact_object_exists: View's context should contain a contact
            object
        test_contact_is_most_recent: View should only return most recent
            contact information
        test_contact_form_unauthenticated_visitor: Form should have no initial
            values if no user.
        test_contact_form_authenticated_visitor: Initial should have `name`
        mapped to user's username if a user is authenticated.

    References:

        * https://docs.djangoproject.com/en/1.11/topics/testing/
        * https://docs.djangoproject.com/en/1.11/topics/testing/tools/

    """

    def setUp(self):
        """
        Create two contact views with different publication dates for testing.
        Create one User to check form initial data populates correctly
        """

        # Create "old" contact info
        self.past_contact = Contact.objects.get_or_create(
            title='title1',
            facebook='https://www.facebook.com',
            github='//www.github.com',
            linkedin='//www.linkedin.com',
            twitter='//www.twitter.com',
            email='jesse.welborn@gmail.com',
            contact_date=timezone.now() - timedelta(days=30)
        )[0]

        # create "new" contact info
        self.current_contact = Contact.objects.get_or_create(
            title='title2',
            facebook='https://www.facebook.com/jwelb',
            github='//www.github.com/jaywelborn',
            linkedin='//www.linkedin.com/--jaywelborn--',
            twitter='//www.twitter.com/__jaywelborn__',
            email='jesse.welborn@gmail.com',
            contact_date=timezone.now(),
        )[0]

        # ensure both items made it to DB
        contact_list = Contact.objects.distinct()
        self.assertEqual(len(contact_list), 2)

        # Create user
        self.user = User.objects.create(
            username='testing',
            email='testing@gmail.com',
        )
        password = 'logmeinplease'
        self.user.set_password(password)
        self.user.save()

        # Make sure user saved properly
        check_user = User.objects.get(username='testing')
        self.assertEqual(self.user, check_user)

    def test_response_code(self):
        """
        View should return response code of 200
        """
        response = self.client.get(reverse('home:contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_object_exists(self):
        """
        Response should have a contact object in its context
        """
        response = self.client.get(reverse('home:contact'))
        self.assertTrue('contact' in response.context)
        self.assertTrue('form' in response.context)

    def test_contact_is_most_recent(self):
        """
        Response should contain the most recent contact object
        """
        response = self.client.get(reverse('home:contact'))
        response_contact = response.context['contact']
        self.assertEqual(response_contact.title,
                         self.current_contact.title)
        self.assertEqual(response_contact.facebook,
                         self.current_contact.facebook)
        self.assertEqual(response_contact.github,
                         self.current_contact.github)
        self.assertEqual(response_contact.linkedin,
                         self.current_contact.linkedin)
        self.assertEqual(response_contact.twitter,
                         self.current_contact.twitter)
        self.assertEqual(response_contact.email,
                         self.current_contact.email)
        self.assertEqual(response_contact.contact_date,
                         self.current_contact.contact_date)

    def test_contact_form_unauthenticated_visitor(self):
        """
        Dictionary `initial` should be empty if no user.
        """

        # get response when no user logged in
        response = self.client.get(reverse('home:contact'))
        self.assertTrue('form' in response.context)

        # ensure form has no initial data
        self.assertNotContains(response, 'value=testing')

    def test_contact_form_authenticated_visitor(self):
        """
        Initial should have `name` mapped to user's username if a
        user is authenticated.
        """

        # log user in
        self.client.login(
            username='testing',
            password='logmeinplease'
        )

        # get response
        response = self.client.get(reverse('home:contact'))
        self.assertTrue('form' in response.context)

        form = response.context['form']
        initial = form.initial
        expected_statement = self.user.username
        self.assertTrue(initial)
        self.assertEqual(initial['name'], expected_statement)
        self.assertTrue('value="{}"'.format(expected_statement) in str(form))


class AboutViewTests(TestCase):
    """Tests for About View.

    Methods:
        test_response: test response contains html from correct template

    """

    def test_response(self):
        response = self.client.get(reverse('home:about'))
        self.assertContains(response, 'About</title>')
