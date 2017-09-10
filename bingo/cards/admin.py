from django.contrib import admin

from .models import BingoCardSquare


# Register your models here.
class BingoCardSquareInline(admin.TabularInline):
    """Tabular inline formset for Bingo Card Squares.

    Fields:
        text: Text to be displayed in the card
        created_date: Date square was created

    References:
        * https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#django.contrib.admin.TabularInline

    """

    model = BingoCardSquare
    extra = 24
    max_num = 24


class BingoCardAdmin(admin.ModelAdmin):
    """Admin interface for BingoCard.

    Fields:
        title: Title of the card
        slug: Slugified title for making pretty urls
        free_space: text for card's `Free Space`. Defaults to `Free Space`
        created_date: Date profile was created
        creator: Creates one to one relationship with Django's built-in User
        private: Boolean allowing users to make their cards invisible to
            unauthenticated site visitors

    Inlines:
        SquareInline: inline form for associating multiple squares with one
            card from the admin panel.

    References:
        * https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User

    """

    fieldsets = [
        ('Bingo Square Info', {'fields': ['title',
                                          'free_space',
                                          'created_date',
                                          'creator',
                                          'private', ]})
    ]
    inlines = [BingoCardSquareInline]
    list_display = ['title', 'created_date', 'private']
    list_filter = ['created_date']
