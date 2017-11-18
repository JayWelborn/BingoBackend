from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views import generic as g
from django.urls import reverse

from social_django.models import UserSocialAuth

from .models import UserProfile
from .forms import RegistrationForm, ProfileEditForm


# Create your views here.
class LoginRedirectView(g.RedirectView):
    """Redirect visitors to appropriate authentication page.

    Attributes:
        permanent: Mark redirect as permanent in HTTP Responses
            (Status Code 301)

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


class ProfileRedirectView(LRM, g.RedirectView):
    """Redirect visitors away from private profiles.

    Attributes:
        pattern_name: name of url to be reversed when redirected.

    MAttributes:
        permanent: Mark redirect as permanent in HTTP Responses
            (Status Code 301)

    Methods:
        dispatch: get pk of authenticated user for verification during
            redirect.
        get_redirect_url: send visitor to profile page if profile is not
            private. Send to Permission Denied view if private.

    References:
    * https://docs.djangoproject.com/en/1.11/ref/class-based-views/base/#redirectview

    """

    permanent = True
    redirect_field_name = None
    login_url = '/profile/login-required/'

    def dispatch(self, request, *args, **kwargs):
        """
        Get pk of authenticated user for use in redirect
        """
        if request.user.is_authenticated:
            self.userprofile_pk = request.user.profile.pk
        return super(ProfileRedirectView, self).dispatch(
            request, *args, **kwargs)

    def get_redirect_url(self, pk):
        """
        Redirect to either detail view or permission denied depending on
        profile's privacy setting.
        """
        profile = UserProfile.objects.get(pk=pk)

        if not profile.private:
            return profile.get_absolute_url()
        elif profile.pk == self.userprofile_pk:
            return profile.get_absolute_url()
        else:
            return reverse('auth_extension:permission_denied')


class RegistrationView(SuccessMessageMixin, g.FormView):
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
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/g-editing/#formview
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/mixins-editing/#django.views.g.edit.FormMixin.get_success_url
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/mixins-editing/#django.views.g.edit.FormMixin.form_valid

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


class ProfileView(LRM, g.DetailView):
    """Allow visitors to view user's profiles

    Attributes:
        model: UserProfile from auth_extension.models. This object will be
            retrieved by PK lookup for page generation
        template_name: Template to use to render data from UserProfile instance
        login_url: redirect users if not authenticated
        redirect_field_name: Stops Django from appending redirect source as
            querystring.
        context_object_name: Name used as key in context dictionary.
        permanent: Sets login redirect as permanent.
        login_url: URL for redirecting unauthenticated users.

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/g-display/#detailview

    """

    model = UserProfile
    template_name = 'auth_extension/profile_view.html'
    redirect_field_name = None
    context_object_name = 'profile'
    permanent = True

    # using reverse causes circular import
    login_url = '/profile/login-required/'


class ProfileEditView(LRM, SuccessMessageMixin, g.FormView):
    """Allow Users to edit their profiles.

    Attributes:
        form_class: Form to render in template
        template_name: Template to use for form rendering
        success_url: Redirect url after successful form completion
        success_message: Message to be displayed after successful form
            completion
        pk: Primary key for currently authenticated user. Passed to form.save()
            method so method can reference current user.
        redirect_field_name: removes querystring applied on redirect for
            unauthenticated users
        login_url: redirect url for unauthenticated users

    Methods:
        dispatch: add user_pk to self for use in get_initial
        get_initial: set initial value for fields to authenticated user's
            profile data if said data is populated.
        form_valid: save form

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/g-editing/#formview

    """

    form_class = ProfileEditForm
    template_name = 'auth_extension/profile_edit.html'
    success_url = '/profile/'
    success_message = 'Profile Updated Successfully!'
    redirect_field_name = None
    login_url = '/profile/login-required/'

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

    def form_valid(self, form):
        """
        Save form.
        """
        form.save(self.user_pk)
        return super(ProfileEditView, self).form_valid(form)


class ProfileListView(g.ListView):
    """View that displays a list of cards.

    Attributes:
        model: Model to list
        context_object_name: Name used in template for readability
        queryset: Sort list of cards by most recent first
        paginate_by: Break list into pages for convenient viewing
        template_name: Template used to render list

    Methods:
        get_queryset: Filter out private cards if user is not authenticated

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-display/#listview

    """

    model = UserProfile
    context_object_name = 'profiles'
    queryset = UserProfile.objects.order_by('-created_date')
    paginate_by = 8
    template_name = 'auth_extension/profile_list.html'

    def get_queryset(self):
        """
        Filter private cards out if user is not authenticated
        """
        queryset = super(ProfileListView, self).get_queryset()

        if self.request.user.is_authenticated:
            return queryset

        else:
            return queryset.filter(private=False)


class Unauthorized(g.TemplateView):
    """View to let unauthenticated users know they need to log in.

    Attributes:
        template_name: template to render

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/base/#templateview

    """
    template_name = 'auth_extension/login_required.html'


class PermissionDenied(g.TemplateView):
    """View to let inform users they have attempted to view a private object.

    Attributes:
        template_name: template to render

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/base/#templateview

    """
    template_name = 'auth_extension/permission_denied.html'


def suggest_profiles(request):
    """Processes AJAX requests from search form in ProfileListView.

    params:
        request: a django request object containing a string `suggestion`

    returns:
        rendered_response: HTML rendering of a list of profiles starting with
            `suggestion`

    """
    profile_list = []
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    users = User.objects.filter(username__istartswith=starts_with)
    users = users.order_by('-date_joined')
    profile_list = [user.profile for user in users]

    return render(request, 'auth_extension/search_results.html',
                  {'profiles': profile_list})


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (
        user.social_auth.count() > 1 or user.has_usable_password()
    )

    return render(request, 'auth_extension/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, 'Your password was successfully updated!'
            )
            return redirect('password')

        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'auth_extension/password.html', {'form': form})
