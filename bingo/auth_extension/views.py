from django.views import generic
from django.urls import reverse

from .models import UserProfile


# Create your views here.
class LoginRedirectView(generic.RedirectView):
    """Redirect visitors to appropriate authentication page.

    Attributes:
        pattern_name: name of url to be reversed when redirected.

    Methods:
        get_redirect_url: send visitor to login page if not authenticated, or
            profile edit page if authenticated.

    References:

    """

    permanent = True

    def get_redirect_url(self):
        """
        Send User to profile edit page if authenticated. Else send visitor
        to login page.
        """
        url = 'auth_extension:login'
        pk = False

        if self.request.user.is_authenticated:
            url = 'auth_extension:profile_edit'
            pk = self.request.user.pk

        if pk:
            return reverse(url, args=[pk])
        else:
            return reverse(url)


class LoginView(generic.TemplateView):
    """Allow visitors to log in.

    Attributes:

    Methods:

    References:

    """

    template_name = 'auth_extension/login.html'


# class RegistrationView(generic.CreateView):
#     """Allow visitors to create and account

#     Attributes:

#     Methods:

#     References:

#     """


# class ProfileView


class ProfileEditView(generic.DetailView):
    """Allow Users to edit their profiles.

    Attributes:

    Methods:

    References:

    """

    model = UserProfile
    template_name = 'auth_extension/profile_edit.html'
