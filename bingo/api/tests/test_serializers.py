import copy

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from auth_extension.models import UserProfile
from cards.models import BingoCard, BingoCardSquare
from home.models import Contact
from api.serializers import (BingoCardSerializer, UserSerializer,
                             UserProfileSerializer, ContactSerializer,
                             BingoCardSquareSerializer)


class UserSerializerTest(APITestCase):
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
        user_updates_username: User should be able to update username without
            affecting other fields.
        user_updates_email: User updating email should not affect other fields.
        user_updates_username_and_email: User should be able to update any 2 of
            the three available fields without affecting the other two.
        user_updates_username_and_password: User should be able to update any 2
            of the three available fields without affecting the other two.
        user_updates_email_and_password: User should be able to update any 2 of
            the three available fields without affecting the other two.

    References:

        * http://www.django-rest-framework.org/api-guide/serializers/

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

        self.profile = UserProfile.objects.create(user=self.user)

    def tearDown(self):
        """
        Clean database so each test starts fresh.
        """
        for user in User.objects.all():
            user.delete()

    def test_serializer_accepts_valid_data(self):
        """
        Serializer should be valid when provided with a username, email and
        password.
        """

        serializer = UserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_password_hashed_for_new_user(self):
        """
        Upon creation, new User's passwords should be hashed before storing
        in the database.
        """

        serializer = UserSerializer(data=self.data)
        if serializer.is_valid():
            user = serializer.save()

        self.assertNotEqual(user.password, self.data['password'])
        self.assertNotEqual(len(user.password), len(self.data['password']))

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
        serializer = UserSerializer(self.user, context={'request': None})
        self.assertNotIn('password', serializer.data)

        included_fields = ['id', 'username', 'bingo_cards', 'profile', 'email']
        for field in included_fields:
            self.assertIn(field, serializer.data)

    def test_user_updates_username(self):
        """
        User updating username should not affect other fields.
        """

        user = User.objects.get(username=self.user.username)
        email = user.email
        userid = user.id
        pk = user.pk
        profile = user.profile
        username = user.username

        update = {
            'username': 'NewUserName',
        }

        serializer = UserSerializer(user, data=update, partial=True,
                                    context={'request': None})
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertTrue(updated_user)
        self.assertEqual(updated_user.username, 'NewUserName')
        self.assertEqual(userid, updated_user.id)
        self.assertEqual(pk, updated_user.pk)
        self.assertEqual(email, updated_user.email)
        self.assertEqual(profile, updated_user.profile)

        self.assertNotEqual(username, updated_user.username)

    def test_user_updates_email(self):
        """
        User updating email should not affect other fields.
        """

        email = self.user.email
        username = self.user.username
        password = self.user.password
        userid = self.user.id
        pk = self.user.pk
        profile = self.user.profile

        update = {
            'email': 'newemail@new.new'
        }

        serializer = UserSerializer(self.user, data=update, partial=True,
                                    context={'request': None})
        # pdb.set_trace()
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertTrue(updated_user)
        self.assertEqual(updated_user.email, update['email'])
        self.assertEqual(updated_user.username, username)
        self.assertEqual(userid, updated_user.id)
        self.assertEqual(pk, updated_user.pk)
        self.assertEqual(password, updated_user.password)
        self.assertEqual(profile, updated_user.profile)
        self.assertNotEqual(email, updated_user.email)

    def test_user_updates_password(self):
        """
        User updating password should have password hashed before storage,
        and update should not affect other fields.
        """

        email = self.user.email
        username = self.user.username
        password = self.user.password
        userid = self.user.id
        pk = self.user.pk
        profile = self.user.profile

        update = {
            'password': 'newtestdude'
        }

        serializer = UserSerializer(self.user, data=update, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertTrue(updated_user)
        self.assertEqual(updated_user.email, email)
        self.assertEqual(updated_user.username, username)
        self.assertEqual(userid, updated_user.id)
        self.assertEqual(pk, updated_user.pk)
        self.assertEqual(profile, updated_user.profile)

        self.assertNotEqual(updated_user.password, update['password'])
        self.assertNotEqual(password, updated_user.password)

    def test_user_updates_username_and_email(self):
        """
        User updating any two fields should not affect the third field.
        """

        email = self.user.email
        username = self.user.username
        password = self.user.password
        userid = self.user.id
        pk = self.user.pk
        profile = self.user.profile

        update = {
            'username': 'multipletest',
            'email': 'multiple@mult.iple'
        }

        serializer = UserSerializer(self.user, data=update, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertTrue(updated_user)
        self.assertEqual(password, updated_user.password)
        self.assertEqual(userid, updated_user.id)
        self.assertEqual(pk, updated_user.pk)
        self.assertEqual(profile, updated_user.profile)

        self.assertNotEqual(updated_user.username, username)
        self.assertNotEqual(updated_user.email, email)

    def test_user_updates_username_and_password(self):
        """
        User updating any two fields should not affect the third field.
        """

        email = self.user.email
        username = self.user.username
        password = self.user.password
        userid = self.user.id
        pk = self.user.pk
        profile = self.user.profile

        update = {
            'username': 'multipletest',
            'password': 'multipleupdatepassword'
        }

        serializer = UserSerializer(self.user, data=update, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertTrue(updated_user)
        self.assertEqual(email, updated_user.email)
        self.assertEqual(userid, updated_user.id)
        self.assertEqual(pk, updated_user.pk)
        self.assertEqual(profile, updated_user.profile)

        self.assertNotEqual(updated_user.username, username)
        self.assertNotEqual(updated_user.password, password)

    def test_user_updates_email_and_password(self):
        """
        User updating any two fields should not affect the third field.
        """

        email = self.user.email
        username = self.user.username
        password = self.user.password
        userid = self.user.id
        pk = self.user.pk
        profile = self.user.profile

        update = {
            'password': 'multipletestthree',
            'email': 'multiple@mult.iple'
        }

        serializer = UserSerializer(self.user, data=update, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertTrue(updated_user)
        self.assertEqual(username, updated_user.username)
        self.assertEqual(userid, updated_user.id)
        self.assertEqual(pk, updated_user.pk)
        self.assertEqual(profile, updated_user.profile)

        self.assertNotEqual(updated_user.password, password)
        self.assertNotEqual(updated_user.email, email)


class UserProfileSerializerTest(APITestCase):
    """Tests for UserProfileSerializer

    Methods:
        setUp: Create User and Profile for testing.
        tearDown: Clean database between tests
        serializer_accepts_valid_data: `is_valid()` should return True when
            instantiated with valid data
        save_updates_correct_fields: Calling `.save()` should update correct
            fields on model
    References:
    """

    def setUp(self):
        """
        Create profile and data for tests.
        """

        self.user = User.objects.create_user(
            username='profileserializertests',
            email='profileserializer@test.com',
            password='passwordtesting'
        )

        self.profile = UserProfile.objects.get_or_create(user=self.user)[0]

        self.data = {
            'website': 'http://www.google.com',
            'about_me': 'I am a test user. I am not real.',
        }

        self.context = {'request': None}

    def tearDown(self):
        """
        Clear database between tests.
        """

        for user in User.objects.all():
            user.delete()

        self.assertEqual(len(UserProfile.objects.all()), 0)

    def test_serializer_accepts_valid_data(self):
        """
        Serializer.is_valid() should return true when instantiated with
        valid data.
        """

        serializer = UserProfileSerializer(
            data=self.data, context=self.context
        )
        self.assertTrue(serializer.is_valid())

    def test_save_updates_correct_fields(self):
        """
        Calling `.save()` should update correct fields on model.
        """
        serializer = UserProfileSerializer(
            self.profile, data=self.data, context=self.context
        )

        if serializer.is_valid():
            new_profile = serializer.save()

        self.assertEqual(new_profile.website, self.data['website'])
        self.assertEqual(new_profile.about_me, self.data['about_me'])
        self.assertEqual(new_profile.user, self.user)

    def test_get_includes_expected_fields(self):
        """
        GET requests should include url, user, created_date, slug, picture,
        website, and about_me fields.
        """

        serializer = UserProfileSerializer(self.profile, context=self.context)
        expeted_fields = ['url', 'user', 'created_date', 'slug', 'website',
                          'about_me']

        for field in expeted_fields:
            self.assertIn(field, serializer.data)


class ContactSerializerTests(APITestCase):
    """ Tests for Contact Serializer.

    Contact serializer is unique in that Contact objects will be edited
    via that Django admin, and so contact objects only need to be read.
    These tests will still test the Serializers ability to write and update
    objects correctly.

    Methods:
        setUp: Create test object
        tearDown: clean test database
        contact_serializes_expected_fields: Serializer should return
            key-value pairs for all fields. Values for missing fields should
            be empty.
        serializer_updates_only_affect_correct_fields: Updates done through
            the serializer should only affect the targeted fields.

    References:

    """

    def setUp(self):
        """
        Create test object.
        """

        self.contact = Contact.objects.get_or_create(
            title='testcontact',
            facebook='www.facebook.com',
            linkedin='www.linkedin.com',
            email='contact@te.st'
        )[0]

        self.context = {'request': None}

        self.data = {
            'github': 'https://www.github.com',
            'facebook': 'https://www.google.com'
        }

    def tearDown(self):
        """
        Clear out test database.
        """
        contacts = Contact.objects.all()
        for contact in contacts:
            contact.delete()

        self.assertEqual(len(Contact.objects.all()), 0)

    def test_contact_serializes_expected_fields(self):
        """
        Serializer should return JSON object with keys for every field. Fields
        blank in the database should have empty values.
        """

        contact_fields = [f.name for f in self.contact._meta.get_fields()]
        serializer = ContactSerializer(self.contact, context=self.context)

        for field in contact_fields:
            self.assertIn(field, serializer.data)

        self.assertFalse(serializer.data['github'])
        self.assertFalse(serializer.data['twitter'])

    def test_serializer_updates_only_affect_correct_fields(self):
        """
        Updates done through serializer should only affect fields included in
        serializers data and leave others unaffected.
        """

        serializer = ContactSerializer(
            self.contact, data=self.data, context=self.context, partial=True
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()

        contact = Contact.objects.latest('contact_date')
        self.assertEqual(self.data['github'], contact.github)
        self.assertEqual(self.data['facebook'], contact.facebook)
        self.assertEqual('testcontact', contact.title)
        self.assertEqual('www.linkedin.com', contact.linkedin)


class BingoCardSquareSerializerTests(APITestCase):
    """Tests for Bingo Card Square Serializer.

    Methods:
        setUp: Create test objects
        tearDown: clean test database
        test_square_serialized_correctly: Serialized squares should have info
            for all fields
        test_update_cannot_write_card: Updates should not be able to write
            card info
        test_update_only_writes_correct_fields: Partial updates should only
            overwrite specified fields.

    References:

    """

    def setUp(self):
        """
        Create test user, card, and squares.
        """

        self.user = User.objects.create_user(
            username='squareserializertest',
            email='square@serial.izer',
            password='password123!'
        )

        self.card = BingoCard.objects.get_or_create(
            title='testing123',
            creator=self.user
        )[0]

        self.squares = []
        for i in range(24):
            self.squares.append(
                BingoCardSquare.objects.get_or_create(
                    card=self.card,
                    text='square-{}'.format(i)
                )[0]
            )

        self.assertEqual(len(self.squares), 24)

        self.context = {'request': None}

    def tearDown(self):
        """
        Clean test database
        """

        for square in BingoCardSquare.objects.all():
            square.delete()

        for card in BingoCard.objects.all():
            card.delete()

        for user in User.objects.all():
            user.delete()

    def test_square_serialized_correctly(self):
        """
        Serialized Suares should include all fields specified.
        """

        for square in self.squares:
            serializer = BingoCardSquareSerializer(
                square, context=self.context
            )

            self.assertEqual(square.id, serializer.data['id'])
            self.assertEqual(square.text, serializer.data['text'])
            self.assertEqual(square.card.title, serializer.data['card'])

    def test_update_cannot_write_card(self):
        """
        Serializer updates should not be able to overwrite the associated card.
        """

        square = self.squares[0]

        data = {
            'text': 'updated square-0',
            'card': 'newtitle'
        }

        serializer = BingoCardSquareSerializer(
            square, data=data, context=self.context, partial=True
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(square.text, data['text'])
        self.assertNotEqual(serializer.data['card'], data['card'])
        self.assertNotEqual(square.card.title, data['card'])

    def test_update_only_writes_correct_fields(self):
        """
        Update should only overwrite included fields.
        """

        data = {
            'text': 'new'
        }
        square = self.squares[0]
        original = {
            'id': square.id,
            'text': square.text,
            'card': square.card.title
        }
        serializer = BingoCardSquareSerializer(
            square, data=data, context=self.context, partial=True
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()
        for key in original.keys():
            self.assertIn(key, serializer.data)
            if key == 'text':
                self.assertNotEqual(serializer.data[key],
                                    original[key])
            else:
                self.assertEqual(serializer.data[key],
                                 original[key])


class BingoCardSerializerTests(APITestCase):
    """Tests for Bingo Card Serializer.

    Methods:
        setUp: create test data
        seralizer_accepts_valid_data: Serializer should accept card with
            title, creator, and 24 squares
        serializer_creates_associated_squares: Serializer should create
            squares associated with card when saved
        serializer_rejects_too_few_squares: Serializer should reject card with
            too few squares, and render appropriate error message.
        partial_update_creates_correct_squares: Updating an existing Bingo Card
            should preserve old squares, and replace text on updated squares.

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

        self.context = {'request': None}

    def tearDown(self):
        """
        Clean test data.
        """

        for square in BingoCardSquare.objects.all():
            square.delete()

        for card in BingoCard.objects.all():
            card.delete()

        for user in User.objects.all():
            user.delete()

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

        serializer = BingoCardSerializer(self.card, context=self.context)

        ids = [square['id'] for square in serializer.data['squares']]
        texts = [square['text'] for square in serializer.data['squares']]

        for square in self.card.squares.all():
            self.assertIn(square.id, ids)
            self.assertIn(square.text, texts)

    def test_partial_update_creates_correct_squares(self):
        """
        Updating an existing Bingo Card should preserve old squares, and
        replace text on updated squares.
        """

        # Retrive complete data to edit
        serializer = BingoCardSerializer(self.card, context=self.context)
        old_data = serializer.data
        data = copy.deepcopy(old_data)
        squares = data['squares']

        # Replace text on 10 squares
        for i in range(10):
            squares[i]['text'] = 'self.card.new    {}'.format(i)

        # Validate serializer with new data
        new_serializer = BingoCardSerializer(
            self.card, data=data, context=self.context, partial=True)
        self.assertTrue(new_serializer.is_valid())
        new_serializer.save()

        card = BingoCard.objects.get(title=self.card.title)

        # Check values for square titles
        for i, square in enumerate(squares):
            self.assertEqual(square['text'], card.squares.all()[i].text)

    def test_partial_update_updates_correct_square_fields(self):
        """
        Updating existing card should change only the fields updated.
        """

        serializer = BingoCardSerializer(self.card, context=self.context)
        old_data = serializer.data
        data = copy.deepcopy(old_data)

        data['title'] = 'Updated'

        new_serializer = BingoCardSerializer(
            self.card, data=data, context=self.context, partial=True
        )

        self.assertTrue(new_serializer.is_valid())
        new_serializer.save()

        for key, value in data.items():
            if key in dir(self.card) and key != 'squares':
                self.assertEqual(str(value), str(getattr(self.card, key)))
