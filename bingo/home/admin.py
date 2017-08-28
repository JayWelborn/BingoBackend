from django.contrib import admin

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    """Admin inteface to update Contact Information.

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

    fieldsets = [
        ('Title', {'fields': ['title',]}),
        ('Social Media URLs', {'fields': ['facebook', 'github', 'linkedin',
                                          'twitter']}),
        ('Email and Date', {'fields': ['email', 'contact_date']})
    ]

    list_display = ['title', 'email', 'contact_date']
    list_filter = ['contact_date']
