from django.contrib.auth.models import User
from django.test import TestCase

from api.serializers import BingoCardSerializer, UserSerializer
from auth_extension.models import UserProfile
from cards.models import BingoCard, BingoCardSquare


class UserSerializerTest(TestCase):
    """Tests for User Serializer.

    Methods:
        setUp: Create test data dictionary
        serializer_accepts_valid_data: Serializer should be valid when provided
            with username, email, and password
        user_and_profile_accepted_upon_save: Serializer should create new
            profile associated with new user
        proper_fields_included_on_retrieval: Password hash should not be sent
            when User object is serialized. Id, username, cards, profile,
            and email should be.

    References:

    """

    def setUp(self):
        """
        Create test dictionary.
        """
        self.data = {
            'username': 'UserSerializerTest',
            'email': 'test@test.test',
            'password': 'password'
        }

        self.user = User.objects.get_or_create(
            username='retrievaltest',
            email='retrieval@retrieve.whatever'
        )[0]
        self.user.set_password('jimothy')
        self.user.save()

    def test_serializer_accepts_valid_data(self):
        """
        Serializer should be valid when provided with a username, email and
        password.
        """

        serializer = UserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_user_and_profile_created_upon_save(self):
        serializer = UserSerializer(data=self.data)
        if serializer.is_valid():
            serializer.save()

        user = User.objects.get(username=self.data['username'])
        profile = UserProfile.objects.get(user=user)
        self.assertTrue(user)
        self.assertTrue(user.profile)
        self.assertEqual(profile.user, user)
        self.assertEqual(user.profile, profile)

    def test_password_not_included_upon_retrieval(self):
        """
        Password should not be included when User is serialized
        """
        serializer = UserSerializer(self.user)
        self.assertNotIn('password', serializer.data)

        included_fields = ['id', 'username', 'bingo_cards', 'profile', 'email']
        for field in included_fields:
            self.assertIn(field, serializer.data)


class BingoCardSerializerTests(TestCase):
    """Tests for Bingo Card Serializer.

    Methods:
        setUp: create test data
        seralizer_accepts_valid_data: Serializer should accept card with
            title, creator, and 24 squares
        serializer_creates_associated_squares: Serializer should create
            squares associated with card when saved
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

        self.card = BingoCard.objects.create(
            title='self.card',
            creator=self.user)

        for i in range(24):
            BingoCardSquare.objects.create(
                text='self.card.square {}'.format(i),
                card=self.card
            )

    def test_serializer_accepts_valid_data(self):
        """
        Serializer.is_valid hsould return true if serializer has title,
        creator, and list of 24 squares.
        """
        serializer = BingoCardSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_creates_associated_squares(self):
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

    def test_serializer_includes_all_squares_with_card(self):
        """
        When existing card is serialized, squares should be included.
        """

        # TODO
        pass
