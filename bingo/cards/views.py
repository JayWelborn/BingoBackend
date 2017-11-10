import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import redirect
from django.views import generic as g
from django.urls import reverse

from .models import BingoCard
from .forms import BingoCardForm, BingoSquareFormset

import pdb


# Create your views here.
class CardListView(g.ListView):
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

    model = BingoCard
    context_object_name = 'bingocards'
    queryset = BingoCard.objects.order_by('-created_date')
    paginate_by = 8
    template_name = 'cards/card_list.html'

    def get_queryset(self):
        """
        Filter private cards out if user is not authenticated
        """
        queryset = super(CardListView, self).get_queryset()

        if self.request.user.is_authenticated:
            return queryset

        else:
            return queryset.filter(private=False)


class MyCardListView(LoginRequiredMixin, g.ListView):
    """View to allow Users to view cards they created.

    Attributes:
        login_url: Url for redirecting unauthenticated visitors
        template_name: Temaplate to render
        context_object_name: Name used in template to access queryset
        redirect_field_name: Remove querystring from login_url upon redirect

    Methods:
        get_queryset: filter queryset to only cards created by current user

    """

    login_url = '/profile/permission-denied/'
    template_name = 'cards/my_cards.html'
    context_object_name = 'cards'
    redirect_field_name = None

    def get_queryset(self):
        """
        Filter queryset to only include cards created by currently
        authenticated user.
        """
        queryset = BingoCard.objects.filter(creator=self.request.user)
        return queryset.order_by('-created_date')


class CardDetailView(g.DetailView):
    """Display full Bingo Card to play.

    Attributes:
        model: The model that will be rendered by the view.
        context_object_name: Name of object to be passed to template
        template_name: HTML template that will render data.

    Methods:
        get: redirect to login-required view if unauthenticated user attempts
            to access private card.

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-display/#detailview

    """

    model = BingoCard
    context_object_name = 'card'
    template_name = 'cards/card_detail.html'

    def get(self, request, *args, **kwargs):
        """
        Redirect if unauthenticated user attempts to view private card.
        """
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        card = context['card']
        if card.private and not request.user.is_authenticated:
            return redirect(reverse('auth_extension:unauthorized'))
        else:
            return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        """
        Add squares to context.
        """
        context = super(CardDetailView, self).get_context_data()
        self.object.squares.all()
        square_set = self.object.squares.all()
        random.shuffle(list(square_set))
        context['squares'] = list(square_set)
        # makes the free space always in the center
        context['squares'].insert(12, self.object.free_space)
        return context


class CardCreateView(LoginRequiredMixin, g.CreateView):
    """Create a new Bingo Card.

    Attributes:
        model: Model associated with view.
        form_class: Form to create the bingo card.
        template_name: Template to be rendered.
        login_url: URL for redirecting unauthenticated users.
        redirect_field_name: Remove querystring from login_url upon redirect.

    Methods:
        get_context_data: Add bingoCardFormset to view's context
        form_valid: Save the formset as well as the form so cards get created
            with squares

    References:
    * https://docs.djangoproject.com/en/1.10/ref/class-based-views/flattened-index/#CreateView
    * https://medium.com/@adandan01/django-inline-formsets-example-mybook-420cc4b6225d
    * https://docs.djangoproject.com/en/1.11/topics/db/transactions/#django.db.transaction.atomic

    """

    model = BingoCard
    form_class = BingoCardForm
    template_name = 'cards/card_create.html'
    login_url = '/profile/permission-denied/'
    redirect_field_name = None

    def get_context_data(self, *args, **kwargs):
        """
        Add formset to context.
        """

        context = super(CardCreateView, self).get_context_data(*args, **kwargs)

        # instantiate formset with data for saving on POST
        if self.request.POST:
            context['square_formset'] = BingoSquareFormset(self.request.POST)

        # instantiate empty formset on GET
        else:
            context['square_formset'] = BingoSquareFormset()

        return context

    def form_valid(self, form):
        """
        Add saving the formset to normal form handling process.
        """

        context = self.get_context_data()
        square_formset = context['square_formset']

        with transaction.atomic():
            # get card instance
            self.object = form.save()
            if square_formset.is_valid():
                # name instance for formset to relate to via ForeignKey
                square_formset.instance = self.object
                square_formset.save()

        return super(CardCreateView, self).form_valid(form)


class CardUpdateView(LoginRequiredMixin, SuccessMessageMixin, g.UpdateView):
    """View for updating already existing cards

    Attributes:
        template_name: Template to render.
        model: Model to be updated.
        form_class: Form to update the Bingo Card.
        login_url: URL for redirecting unauthenticated users.
        redirect_field_name: Remove querystring from login_url upon redirect.
        success_message: Message to be displayed on successful update

    Methods:
        get_context_data: Add formset to context with data and instance as
            needed.
        post: Add formset validation to form validation. Reject both if either
            is invalid.
        form_valid: Save formset along with form.
        form_invalid: Render same page with error messages.

    References:
        * https://groups.google.com/forum/#!topic/django-users/yS8mXXGhJY0
        * https://github.com/timhughes/django-cbv-inline-formset/blob/master/music/views.py

    """

    model = BingoCard
    form_class = BingoCardForm
    template_name = 'cards/card_update.html'
    login_url = '/profile/permission-denied/'
    redirect_field_name = None
    success_message = 'Card Updated Successfully'

    def get_context_data(self, *args, **kwargs):
        """
        Add formset to context.
        """

        context = super(CardUpdateView, self).get_context_data(*args, **kwargs)

        # give formset data and instance on POST
        if self.request.POST:
            context['square_formset'] = BingoSquareFormset(
                self.request.POST,
                instance=self.object
            )

        # give formset instance on GET
        else:
            context['square_formset'] = BingoSquareFormset(
                instance=self.object
            )

        return context

    def post(self, *args, **kwargs):
        """
        Add formset validation to POST. Reject form and formset if either is
        invalid.
        """

        # Get object, form, and formset
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = BingoSquareFormset(self.request.POST)

        # Validate form and formset
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)

        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        """
        Update objects if form and formset are valid.
        """

        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form, formset):
        """
        Reject form and formset if either are invalid.
        """
        return self.render_to_response(
            self.get_context_data(
                form=form,
                formset=formset
            )
        )
