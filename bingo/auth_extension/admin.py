from django.contrib import admin


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    """Admin inteface for UserProfiles.

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

    fieldsets = [
        ('User', {'fields': ['user']}),
        ('Optional Profil Information', {'fields': ['picture', 'website',
                                                    'about_me']}),
        ('Control Info', {'fields': ['created_date', 'private']})
    ]

    list_display = ['user', 'created_date', 'private']
    list_filter = ['created_date']
