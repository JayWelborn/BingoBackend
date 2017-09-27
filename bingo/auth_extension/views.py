from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.urls import reverse
from django.utils.decorators import method_decorator

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
        get_success_url: overrides success_url with url for EditProfile view
            of profile associated with authenticated user.

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-editing/#formview
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.get_success_url
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_valid

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

    def get_success_url(self, **kwargs):
        """
        Get url for ProfileEditView for authenticated user
        """
        current_user = self.request.user
        return reverse(
            'auth_extension:profile_edit',
            args=[current_user.profile.pk]
        )


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class ProfileEditView(SuccessMessageMixin, generic.FormView):
    """Allow Users to edit their profiles.

    Attributes:
        form_class: Form to render in template
        template_name: Template to use for form rendering
        success_url: Redirect url after successful form completion
        success_message: Message to be displayed after successful form
            completion
        pk: Primary key for currently authenticated user. Passed to form.save()
            method so method can reference current user.

    Methods:
        __init__: add authenticated user's pk as an instance-level variable
        dispatch: add user_pk to self for use in get_initial
        get_initial: set initial value for fields to authenticated user's
            profile data if said data is populated.

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-editing/#formview

    """

    form_class = ProfileEditForm
    template_name = 'auth_extension/profile_edit.html'
    success_url = '/profile'
    success_message = 'Profile Updated Successfully!'

    def dispatch(self, request, *args, **kwargs):
        """
        Get pk of authenticated user for use in the form
        """
        self.user_pk = request.user.pk
        return super(ProfileEditView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Populate form with data from currently authenticate User's profile.
        """
        initial = super(ProfileEditView, self).get_initial()

        if self.request.user.profile:
            profile = self.request.user.profile
            initial['picture'] = profile.picture
            initial['website'] = profile.website
            initial['private'] = profile.private
            initial['about_me'] = profile.about_me

        return initial

    # def form_valid(self):


# TODO *** ProfileListView ***
