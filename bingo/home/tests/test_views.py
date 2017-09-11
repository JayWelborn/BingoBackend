from django.test import TestCase

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

        # create public and private cards for each user
        self.cards = []
        for user in self.users:
            title = user.username
            new_card = create_card(title, user, True)
            self.cards.append(new_card)

        for user in self.users:
            title = user.username
            new_card = create_card(title, user, False)
            self.cards.append(new_card)
