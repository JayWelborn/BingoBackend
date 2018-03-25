from django.contrib.auth.models import User

from auth_extension.models import UserProfile
from cards.models import BingoCard

import pdb


def create_user(username, password, private):
    """Create User object with associated Profile.

    Args:
        username (str): String to be stored as user's username.
        private (bool): Indicates whether Profile should be private or not.

    Returns:
        User (User): Reference to created user object with associated profile.

    """

    # create User
    user = User.objects.get_or_create(
        username=username,
        email='{}@gmail.com'.format(username)
    )[0]
    user.set_password(password)

    # create Profile
    profile = UserProfile.objects.get_or_create(
        user=user,
    )[0]
    profile.private = private
    user.profile = profile

    user.save()
    profile.save()

    return user


def create_card(title, user, private=False):
    """Create BingoCard object with associated Creator.

    Args:
        title (str): String to be stored as card's title.
        user (User): User to be set as card's creator.
        private (bool): Indicates whether BingoCard should be private or not.

    Returns:
        card (BingoCard): Reference to created BingoCard object.

    """

    # create and return card
    card = BingoCard.objects.get_or_create(
        title=title,
        creator=user,
        private=private
    )[0]

    return card
