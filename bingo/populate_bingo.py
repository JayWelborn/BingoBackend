import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'bingo.settings'

import django
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone

from home.models import Contact
from cards.models import BingoCard, BingoCardSquare
from auth_extension.models import UserProfile


def main():
    print('Populating Users and Profiles...')
    populate_users()
    print('Populating Contact...')
    populate_contact()
    print('Populating Cards...')
    populate_cards()


def populate_users():
    """Populates database with example users.

    Creates Dictionary of Dictionaries representing Users. Next creates
    dictionaries mapping Profiles to Users. Finally iterates
    through dictionaries creating and linking Users to Profiles.
    """

    users = {
        'Rick': {
            'username': 'RickSanchez',
            'password': 'M0rty-!5-My-53Cre7-CR|_|5|-|',
            'email': 'plumbusdinglebop@gmail.com'
        },
        'Morty': {
            'username': 'MortySmith',
            'password': 'R!cK-r|-|ymes-w!7h-|]![|<',
            'email': 'mortyismyrealname@aol.com'
        },
        'Jerry': {
            'username': 'JerrySmith',
            'password': 'iamverysmartandbrave',
            'email': 'bethismean@hotmail.com'
        },
        'Beth': {
            'username': 'BethSmith',
            'password': 'vetsarerealdoctos',
            'email': 'Beth.Smith.Is.A.Real.Doctor@gmail.com'
        }
    }

    profiles = [
        {
            'user': users['Rick'],
            'website': 'http://rickandmorty.wikia.com/wiki/Rick_Sanchez',
            'private': False,
            'about_me': """Not much is known about Rick's life before his
                           current state seen in the show except for a few
                           things that have been vaguely mentioned in the
                           series. It has been mentioned multiple times that
                           Rick has been absent from the family for at least
                           fourteen years and it wasn't until one year before
                           the events of "Something Ricked This Way Comes" when
                           Rick finally returned to the Smith house on January
                           15th.[4] The reason for his absence is unknown to
                           the rest of the family."""
        },
        {
            'user': users['Morty'],
            'website': 'http://rickandmorty.wikia.com/wiki/Morty_Smith',
            'private': False,
            'about_me': """Mortimer "Morty" Smith Sr. is one of the two
                           eponymous main protagonists in Rick and Morty.
                           He is the grandson of Rick and is often forced to
                           tag along on his various misadventures. Morty
                           attends Harry Herpson High School along with his
                           sister, Summer. """
        },
        {
            'user': users['Jerry'],
            'website': 'http://rickandmorty.wikia.com/wiki/Jerry_Smith',
            'private': True,
            'about_me': """Jerry Smith is the ex-husband of Beth Smith, and the
                           father to Summer Smith and a deceased Morty. Though,
                           he currently acts as the father, and son-in-law, of
                           the Morty Smith and Rick Sanchez from Dimension
                           C-137, respectively. Jerry always tries to think of
                           the best interest of the family, but his attempt to
                           be the patriarch of the family can often be
                           misguided by his self-centered nature. This causes
                           him a great deal of conflict with Rick, as his
                           father-in-law clearly has no respect for him
                           whatsoever."""
        },
        {
            'user': users['Beth'],
            'website': 'http://rickandmorty.wikia.com/wiki/Beth_Smith',
            'private': True,
            'about_me': """Beth Smith (née Sanchez) is the daughter of a
                           deceased Rick Sanchez, the wife of Jerry Smith, and
                           the mother of Summer Smith and a deceased Morty.
                           Though, she currently acts as the mother, and
                           daughter, of the Morty Smith and Rick Sanchez from
                           Dimension C-137, respectively. Sanctimonious and
                           above others, she struggles with her husband over
                           his contributions, due in part to his lower-level
                           position, further driven by her father influencing
                           her feelings of superiority. """
        }
    ]

    for profile in profiles:
        add_profile(profile['user'],
                    profile['website'],
                    profile['private'],
                    profile['about_me'])


def populate_contact():
    """Populates database with example Contact object.

    Creates single Contact object for dev database.
    """

    contact = Contact.objects.get_or_create(
        title='Contact',
        facebook='https://www.facebook.com/JayWelb',
        github='https://www.github.com/jaywelborn',
        linkedin='https://www.linkedin.com/in/--jaywelborn--/',
        twitter='https://twitter.com/__JayWelborn__',
        email='jesse.welborn@gmail.com',
    )[0]

    contact.save()


def populate_cards():
    """Create Cards for dev database.

    Gets list of Users to act as cards' `creators`. Creates one
    Card per user, with 24 squares with ints between 0 and 23 as
    their text.
    """

    cards = []
    users = User.objects.all()

    for user in users:
        cards.append(add_card(user))

    for card in cards:
        card = add_squares(card)


def add_profile(user, website, private, about):
    """Save User and Profile to Database.

    Args:
        user (User): dictionary of values associated with django's User.
        date (DateTime): datetime object.
        website (str): url of website for user's profile.
        private (bool): marks profile as private. defaults to `False`
        about (str): bio for profile.
    """

    new_user = User.objects.get_or_create(
        username=user['username'],
        email=user['email'])[0]
    new_user.set_password(user['password'])
    new_user.save()

    profile = UserProfile.objects.get_or_create(
        user=new_user,
        website=website,
        private=private,
        about_me=about)[0]

    profile.save()


def add_card(user):
    """Add Card to database for given user.

    Args:
        user (User): User object to be used as Card's `creator`.

    Returns:
        card (BingoCard): BingoCard object with fields populated
                          based on given user.

    """

    title = 'Bingo Card Created by {}'.format(user.username)
    card = BingoCard.objects.get_or_create(
        title=title,
        creator=user,
    )[0]
    card.save()
    return card


def add_squares(card):
    """Add squares to new card.

    Args:
        card (BingoCard): BingoCard object to be populated.

    Returns:
        card (BingoCard): BingoCard with squares added.

    """

    for i in range(24):
        square = BingoCardSquare.objects.create(
            text=str(i),
            card=card,
        )
        square.save()

    return card


if __name__ == '__main__':

    main()
