from django.contrib.admin import sites
from django.contrib.auth.models import User, Group

from home.admin import ContactAdmin
from home.models import Contact

from auth_extension.admin import UserProfileAdmin
from auth_extension.models import UserProfile

from cards.admin import BingoCardAdmin
from cards.models import BingoCard


class BingoAdmin(sites.AdminSite):
    """Admin Site with customized header and title bar.

    References:

        * https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#customizing-the-adminsite-class

    """
    site_header = 'Bingo Administration'
    site_title = 'Bingo Administration'


bingo_admin_site = BingoAdmin(name='admin')

bingo_admin_site.register(User)
bingo_admin_site.register(Group)
bingo_admin_site.register(Contact, ContactAdmin)
bingo_admin_site.register(UserProfile, UserProfileAdmin)
bingo_admin_site.register(BingoCard, BingoCardAdmin)
