from django.contrib.auth.models import User
from django.test import TestCase

from api.serializers import BingoCardSerializer
from cards.models import BingoCard, BingoCardSquare


class BingoCardSerializerTests(TestCase):
    """Tests for Bingo Card Serializer.

    Methods:
        setUp: create test data
        seralizer_accepts_valid_data: Serializer should accept card with
            title, creator, and 24 squares
        serializer_rejects_too_few_squares: Serializer should reject card with
            too few squares, and render appropriate error message.

    References:

    """

    def setUp(self):
        """
        Create objects for testing
        """

        self.user = User.objects.get_or_create(
            username='test',
            email='test@test.testing'
        )[0]
        self.user.set_password('password')
        self.user.save()

        squares = []
        for i in range(24):
            squares.append({'text': 'square {}'.format(i)})

        self.valid_data = {
            'title': 'test title',
            'creator': self.user,
            'squares': squares
        }

        new_squares = squares
        new_squares = new_squares[:5]

        self.invalid_data = self.valid_data.copy()
        self.invalid_data['squares'] = new_squares

    def test_serializer_accepts_valid_data(self):
        """
        Serializer.is_valid hsould return true if serializer has title,
        creator, and list of 24 squares.
        """
        serializer = BingoCardSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_creates_objects_correctly(self):
        """
        Seralizer should create Bingo Card and 24 cards related to parent
        Bingo Card.
        """
        serializer = BingoCardSerializer(data=self.valid_data)
        if serializer.is_valid():
            serializer.save(creator=self.user)

        card = BingoCard.objects.get(title=self.valid_data['title'])
        self.assertTrue(card)
        self.assertTrue(card.squares)
        self.assertEqual(card.title, self.valid_data['title'])

        for s in self.valid_data['squares']:
            square = BingoCardSquare.objects.get(text=s['text'])
            self.assertTrue(square)
            self.assertIn(square, card.squares.all())
            self.assertEqual(square.card, card)

    def test_serializer_rejects_too_few_cards(self):
        """
        Serializer should reject data with too few Bingo Squares. Error message
        should read "Must have exactly 24 squares"
        """
        serializer = BingoCardSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Must have exactly 24 squares',
                      serializer.errors['squares'])
