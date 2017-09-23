from django.contrib.auth import authenticate, login
from django.views import generic
from django.urls import reverse

from .models import UserProfile
from .forms import RegistrationForm


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


class RegistrationView(generic.FormView):
    """Allow visitors to create and account

    Attributes:

    Methods:

    References:

    """
    template_name = 'registration/registration_form.html'
    form_class = RegistrationForm
    success_url = '/profile'

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

    Methods:

    References:

    """

    model = UserProfile
    template_name = 'auth_extension/profile_view.html'


class ProfileEditView(generic.DetailView):
    """Allow Users to edit their profiles.

    Attributes:

    Methods:

    References:

    """

    model = UserProfile
    template_name = 'auth_extension/profile_edit.html'
