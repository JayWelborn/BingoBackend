from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.
class UserProfile(models.Model):
    """Model to store User Profile Information.

    Fields:
        user: Creates one to one relationship with Django's built-in User
        picture: Profile picture for user
        website: URL for personal website or social media site
        private: Allows users to set their profiles to private
        about_me: Users can write a short bio of themselves for display

    References:

        * https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User

    """
    user = models.OneToOneField(User, related_name='profile')
    picture = models.ImageField(upload_to='profile_images', blank=True)
    website = models.URLField(blank=True)
    private = models.BooleanField(default=False)
    about_me = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return self.user.username
