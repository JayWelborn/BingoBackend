# django imports
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext as _

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

    Methods:
        clean: perform normal clean operations. Additionally ensure passwords
            match and are valid
        save: save both user and matching profile

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

    def clean(self):
        """
        Perform default clean behavior, then ensure passwords match and are
        validated by AUTH_PASSWORD_VALIDATORS.
        """
        self.is_valid()
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data['password']
        password_confirmation = cleaned_data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError(
                _('Passwords entered do not match.'),
                code='invalid'
            )

        validate_password(password=password)

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
                raise forms.ValidationError('Passwords entered do not match.')

            profile = UserProfile.objects.create(user=user)
            profile.save()
            return self

        else:
            return self.errors


class ProfileEditForm(CrispyBaseModelForm):
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
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'profile_form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', 'Edit Profile'))

    def save(self, pk):
        """ Updates UserProfile if it exists, creates new instance if it
            doesn't.

        Args:
            self: instance of ProfileEditForm
            pk: Primary Key attribute of UserProfile's related User instance

        Returns:
            self: instance of ProfileEditForm after saving

        """

        # validate form and get cleaned data
        if self.is_valid():
            picture = self.cleaned_data['picture']
            website = self.cleaned_data['website']
            private = self.cleaned_data['private']
            about_me = self.cleaned_data['about_me']

        else:
            return self.errors

        # get user and profile for editing
        user = User.objects.get(pk=pk)
        profile = UserProfile.objects.get_or_create(user=user)[0]

        # assign form values to related fields in profile
        if picture:
            profile.picture = picture

        if website:
            profile.website = website

        if private:
            profile.private = private

        if not private:
            profile.private = False

        if about_me:
            profile.about_me = about_me

        profile.save()

        return self
