from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.test import TestCase

from cards.models import BingoCard, BingoCardSquare


# Create your tests here.
class BingoCardModelTests(TestCase):
    """Tests for BingoCard Model.

    Methods:
        setUp: Creates BingoCard to test against
        test_slugify_on_save: Calling BingoCard.save() should set
            BingoCard.slug to a slugified version of BingoCard.title
        test_squares_relate_to_card: All squares created in setUp should be
            related to card created in setUp.
        test_user_accessible_from_card: User should be stored as
            BingoCard.creator
        test_user_accessible_from_square: User should be accessible from square
            at square.card.creator

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/

    """

    def setUp(self):
        """
        Create instance(s) for tests
        """
        self.test_user = User.objects.create(username='Test User',
                                             email='test@email.com')
        self.test_user.set_password('test_password_678!!!')
        self.public_bingo_card = BingoCard.objects.create(
            title='Test Card',
            creator=self.test_user
        )

        for i in range(24):
            BingoCardSquare.objects.create(
                text=str(i),
                card=self.public_bingo_card
            )

    def test_slugify_on_save(self):
        """
        Title should be properly slugified when object is saved
        """
        test_slug = slugify(self.public_bingo_card.title)
        card_slug = self.public_bingo_card.slug
        self.assertEqual(test_slug, card_slug)
        self.assertEqual(card_slug, 'test-card')

    def test_squares_relate_to_card(self):
        """
        All Squares should relate to the test card
        """
        for square in self.public_bingo_card.squares.all():
            self.assertEqual(square.card, self.public_bingo_card)

    def test_user_accessible_from_card(self):
        """
        User should be accessible from BingoCard via card.creator
        """
        self.assertEqual(self.test_user, self.public_bingo_card.creator)

    def test_user_accessible_from_square(self):
        """
        User should be accessible from BingoCardSquare via square.card.creator
        """
        square = BingoCardSquare.objects.latest('created_date')
        self.assertEqual(self.test_user, square.card.creator)


class BingoCardSquareModelTests(TestCase):
    """Tests for BingoCardSquare Model

    Methods:
        setUp: Creates BingoCard with Squares to test against
        test_squares_relate_to_card: All squares created in setUp should be
            related to card created in setUp.
        test_user_accessible_from_square: User should be accessible from square
            at square.card.creator
        test_square_stringifies_correctly: Calling str() on Square instance
            should return properly legible text

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/

    """

    def setUp(self):
        """
        Create instance(s) for tests
        """
        self.test_user = User.objects.create(username='TestUser',
                                             email='test@email.com')
        self.test_user.set_password('test_password_678!!!')
        self.public_bingo_card = BingoCard.objects.create(
            title='Test Card',
            creator=self.test_user
        )

        for i in range(24):
            BingoCardSquare.objects.create(
                text=str(i),
                card=self.public_bingo_card
            )

    def test_squares_relate_to_card(self):
        """
        All Squares should relate to the test card
        """
        for square in self.public_bingo_card.squares.all():
            self.assertEqual(square.card, self.public_bingo_card)

    def test_user_accessible_from_square(self):
        """
        User should be accessible from BingoCardSquare via square.card.creator
        """
        for square in BingoCardSquare.objects.all():
            self.assertEqual(self.test_user, square.card.creator)

    def test_square_stringifies_correctly(self):
        """
        Calling str() on Square should return related card'ss title and
        square's text.
        """

        for square in BingoCardSquare.objects.all():
            self.assertEqual(str(square), '{}: {}'.format(square.card.title,
                                                          square.text))
