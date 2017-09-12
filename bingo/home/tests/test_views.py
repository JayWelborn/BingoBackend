from django.test import TestCase
from django.urls import reverse

from cards.models import BingoCard

from .helpers import create_user, create_card


# Start test classes
class IndexViewTests(TestCase):
    """Tests for Index View

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
        self.assertEqual(True, 'card_list' in response.context)

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
            self.assertEqual(card in qs, True)

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
            self.assertEqual(card in qs, True)
