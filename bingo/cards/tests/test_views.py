from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cards.models import BingoCard, BingoCardSquare


class CardListViewTests(TestCase):
    """Tests for CardListView class

    Methods:
        setUp: Create cards for testing
        test_template_used: View should use `cards/card_list.html`
            and return 200
        test_context_object_name: List of cards should be in
            context['bingocards']
        test_cards_sorted_correctly: Cards should be sorted most recent first

    References:
        * https://www.obeythetestinggoat.com/book/appendix_Django_Class-Based_Views.html

    """

    def setUp(self):
        """
        Create objects for testing
        """

        self.user = User.objects.create(
            username='cardviewtests',
            email='cardviewtest@gmail.com'
        )
        self.user.set_password('c@RdviewTe5t5')
        self.user.save()

        self.assertTrue(self.user)

        # Create bingocards
        self.cards = []
        for i in range(10):
            card = BingoCard.objects.create(
                title='card # {}'.format(i),
                created_date=timezone.now() - timedelta(days=i),
                creator=self.user,
            )
            card.save()
            self.cards.append(card)

        self.assertEqual(len(self.cards), 10)

    def test_template_used(self):
        """
        View shoud use `cards/card_list.html`.
        """

        response = self.client.get(reverse('cards:card_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'cards/card_list.html'
        )
