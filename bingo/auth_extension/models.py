from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class UserProfile(models.Model):
    """Model to store User Profile Information.

    Fields:
        user: Creates one to one relationship with Django's built-in User
        created_date: Date profile was created
        picture: Profile picture for user
        website: URL for personal website or social media site
        private: Allows users to set their profiles to private
        about_me: Users can write a short bio of themselves for display

    References:

        * https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User

    """

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    user = models.OneToOneField(
        User,
        related_name='profile',
        # TODO - test on_delete
        on_delete=models.CASCADE,
    )

    created_date = models.DateField(
        default=timezone.now
    )

    slug = models.SlugField()

    picture = models.ImageField(
        upload_to='profile_images',
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    private = models.BooleanField(
        default=False
    )

    about_me = models.TextField(
        max_length=140,
        blank=True,
    )

    def __str__(self):
        """
        Calling __str__ will return something legible.
        """
        return self.user.username

    def save(self, *args, **kwargs):
        """
        Slugifies username automatically when UserProfile is saved
        """
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Return url for viewing a specific profile
        """
        return reverse('auth_extension:profile_view', args=[self.pk])
