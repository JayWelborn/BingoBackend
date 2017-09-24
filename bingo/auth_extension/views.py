from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.urls import reverse

from .models import UserProfile
from .forms import RegistrationForm, ProfileEditForm


# Create your views here.
class LoginRedirectView(generic.RedirectView):
    """Redirect visitors to appropriate authentication page.

    Attributes:
        pattern_name: name of url to be reversed when redirected.

    Methods:
        get_redirect_url: send visitor to login page if not authenticated, or
            profile edit page if authenticated.

    References:
    * https://docs.djangoproject.com/en/1.11/ref/class-based-views/base/#redirectview

    """

    permanent = True

    def get_redirect_url(self):
        """
        Send User to profile edit page if authenticated. Else send visitor
        to login page.
        """
        url = 'registration:auth_login'
        pk = False
        current_user = self.request.user

        if current_user.is_authenticated:
            url = 'auth_extension:profile_edit'

            try:
                pk = current_user.profile.pk

            except UserProfile.DoesNotExist:
                new_profile = UserProfile.objects.create(user=current_user)
                new_profile.save()
                pk = new_profile.pk

        if pk:
            return reverse(url, args=[pk])
        else:
            return reverse(url)


class RegistrationView(SuccessMessageMixin, generic.FormView):
    """Allow visitors to create and account

    Attributes:
        form_class: Form to be rendered. RegistrationForm allows new users to
            create accounts.
        template_name: Template to render the form
        success_url: URL where users are redirected upon successful account
            creation. In this case, they go to the base view of the
            auth_extnsion app, which acts as a filter redirecting users based
            on various criteria.
        success_message: message to be displayed upon successful form
            submission

    Methods:
        form_valid: calls form.save(), then authenticates new user before
            sending them to success_url

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-editing/#formview

    """
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'
    success_url = '/profile'
    success_message = 'Your account has been created successfully. Please' + \
        'take a moment to share a bit more about yourself.'

    def form_valid(self, form):
        """
        saves form, logs new user in, and returns HttpResponse
        """
        form = form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return super(RegistrationView, self).form_valid(form)


class ProfileView(generic.DetailView):
    """Allow visitors to view user's profiles

    Attributes:
        model: UserProfile from auth_extension.models. This object will be
            retrieved by PK lookup for page generation
        template_name: Template to use to render data from UserProfile instance

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-display/#detailview

    """

    model = UserProfile
    template_name = 'auth_extension/profile_view.html'


class ProfileEditView(SuccessMessageMixin, generic.FormView):
    """Allow Users to edit their profiles.

    Attributes:

    Methods:

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-editing/#formview

    """

    form_class = ProfileEditForm
    template_name = 'auth_extension/profile_edit.html'
    success_url = '/profile'
    success_message = 'Profile Updated Successfully!'
