from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone


# Create your models here.
class BingoCard(models.Model):
    """Model to store Bingo Card information.

    Fields:
        title: Title of Bingo Card.
        slug: Slugified title for pretty urls
        free_space: Text for the center square of the Bingo Card. Defaults to
            `Free Space`.
        created_date: Date Card was created.
        creator: Foreign key for User who created the Bingo Card.
        private: Boolean field allowing user to mark Bingo Card private or
            public. All cards will be visible to authenticated users, this only
            determines if the card will also be visible to the unauthenticated
            public.
        squares: Reverse one-to-many lookup for `squares` object.

    References:

        * https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User
        * https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_one/

    """

    class Meta:
        verbose_name = 'Bingo Card'
        verbose_name_plural = 'Bingo Cards'

    title = models.CharField(
        'Title of the Bingo Card',
        max_length=50,
    )

    slug = models.SlugField()

    free_space = models.CharField(
        'Free Space text will be shown in the center of your Bingo Card',
        max_length=40,
        default='Free Space',
    )

    created_date = models.DateField(
        default=timezone.now,
    )

    creator = models.ForeignKey(
        User,
        related_name='bingo_cards',
        on_delete=models.CASCADE,
    )

    private = models.BooleanField(
        default=False,
    )

    def __str__(self):
        """
        Calling __str__ will return something legible.
        """
        return self.title

    def save(self, *args, **kwargs):
        """
        Slugifies title automatically when BingoCard is saved
        """
        self.slug = slugify(self.title)
        super(BingoCard, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Get url to view card.
        """

        from django.urls import reverse
        return reverse('cards:card_detail', args=[self.pk])


class BingoCardSquare(models.Model):
    """Model to store text for Bingo Card Squares.

    Fields:
        text: Text for Square on `BingoCard`.
        card: ForeignKey for related `BingoCard`.

    References:

        * https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User
        * https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_one/

    """

    class Meta:
        verbose_name = 'Bingo Square'
        verbose_name_plural = 'Bingo Squares'

    text = models.CharField(
        'Text will be shown in a square of your Bingo Card',
        max_length=40,
    )

    card = models.ForeignKey(
        BingoCard,
        related_name='squares',
        on_delete=models.CASCADE,
    )

    created_date = models.DateField(
        default=timezone.now,
    )

    def __str__(self):
        """
        Calling __str__ will return something legible.
        """
        string = '{}: {}'.format(self.card.title, self.text)
        return string
