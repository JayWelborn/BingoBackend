from django.test import TestCase

from .helpers import create_user, create_card


class CreateUserTests(TestCase):
    """Tests for create_user helper function.

    Methods:
        test_private_user_is_private: When bool `private=True`, created User
            is associated with a private profile.
        test_public_user_is_public: When bool `private=False`, created User
            is associated with a public profile.

    """

    def test_private_user_is_private(self):
        """
        Create User with private Profile
        """
        user = create_user('private', 'something123!@#', True)
        self.assertEqual(user.profile.private, True)

    def test_public_user_is_public(self):
        """
        Create User with public Profile
        """
        user = create_user('public', 'somethingelse123!@#', False)
        self.assertEqual(user.profile.private, False)


class CreateCardTests(TestCase):
    """Tests for create_card helper function.

    Methods:
        test_private_card_is_private: When bool `private=True`, card.private
            should return True.
        test_public_card_is_public: When bool `private=False`, card.private
            should return False.

    """

    def test_private_card_is_private(self):
        """
        Create private Card
        """
        user = create_user('public', 'somethingelse123!@#', False)
        card = create_card('private', user, True)
        self.assertEqual(card.private, True)

    def test_public_card_is_public(self):
        """
        Create Public Card
        """
        user = create_user('public', 'somethingelse123!@#', False)
        card = create_card('public', user, False)
        self.assertEqual(card.private, False)
