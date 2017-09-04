from django.db import models
from django.utils import timezone

# Create your models here.
class Contact(models.Model):
    """Model to store Contact Information.

    Fields:
        title: Title to display on browser tab header
        facebook: URL for Facebook link on contact page
        github: URL for GitHub link on contact page
        linkedin: URL for LinkedIn link on contact page
        twitter: URL for Twitter link on contact page
        email: Creator's email address
        contact_date: Date contact info was last update

    References:

        * none

    """

    class Meta:
        verbose_name_plural = 'Contact'

    title = models.CharField(
        'Title to display on browser tab header',
        max_length=30
    )

    facebook = models.URLField(
        'URL for Facebook Page',
        blank=True
    )

    github = models.URLField(
        'URL for GitHub Profile',
        blank=True
    )

    linkedin = models.URLField(
        'URL for LinkedIn profile',
        blank=True
    )

    twitter = models.URLField(
        'URL for Twitter Profile',
        blank=True
    )

    email = models.EmailField()

    contact_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title
