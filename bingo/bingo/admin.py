from django.contrib import admin
from django.contrib.auth.models import User, Group

from home.admin import ContactAdmin
from home.models import Contact

class BingoAdmin(admin.sites.AdminSite):
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