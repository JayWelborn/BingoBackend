# django imports
from django import forms
from django.contrib.auth.models import User

# third party imports
from crispy_forms.layout import Submit

# app imports
from bingo.forms import CrispyBaseModelForm

# relative imports
from .models import UserProfile


class RegistrationForm(CrispyBaseModelForm):
    """Form for registering new users. Only contains fields required
    for user objects. Redirect will take users to page where they can
    edit their profiles.

    Fields:
        username: User's name. Will be slugified for URL upon form save
        email: User's email address
        password: Password. Hashed before storing in the database.

    References:
        * https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#modelform

    """

    # specify widget for password input
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'registration_form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', 'Register'))

    class Meta:
        model = User
        fields = ('username', 'email',)

    def save(self):
        """
        Here we override the parent class's 'save' method to create a
        UserProfile instance matching the User in the form.
        """
        if self.is_valid():
            user = User.objects.create(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
            )

            password = self.cleaned_data['password']
            password_confirmation = self.cleaned_data['password_confirmation']

            if password and password == password_confirmation:
                user.set_password(self.cleaned_data['password'])
                user.save()

            else:
                raise forms.ValidationError('Passwords Entered Do Not Match')

            profile = UserProfile.objects.create(user=user)
            profile.save()
            return user

        else:
            return self.errors


class ProfileForm(CrispyBaseModelForm):
    """Form for editing authenticated user's profile.
    On success, will redirect to update DetailView for
    user's profile.

    Fields:
        picture: User's profile picture
        website: User's website url
        about: User's bio
        private: Boolean. Determines whether User's profile will be visible
            to the public.

    References:
        * https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#modelform

    """
    class Meta:
        model = UserProfile
        fields = ('picture', 'website', 'private', 'about_me')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'profile_form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', 'Edit Profile'))
