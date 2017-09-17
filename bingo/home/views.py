# django imports
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

# app imports
from cards.models import BingoCard

# relative imports
from .models import Contact
from .forms import ContactForm


# Create your views here.
class IndexView(generic.ListView):
    """Home Page View.

    Displays a list of 5 Bingo Cards sorted by creation date: most recent cards
    first. If user is authenticated, this will include private cards. If not,
    only cards not marked private will be displayed.

    Attributes:
        model: Model to be listed.
        template_name: Template to render.
        context_object_name: name used to refer to list in template

    Methods:
        get_queryset: filters out private objects if user is not authenticated

    References:
        * https://docs.djangoproject.com/en/1.11/topics/class-based-views/generic-display/

    """

    model = BingoCard
    template_name = 'home/index.html'
    context_object_name = 'card_list'

    def get_queryset(self):
        """
        Returns 5 most recent cards, filtered by privacy setting.
        """
        if self.request.user.is_authenticated():
            return BingoCard.objects.distinct().order_by('-created_date')[:5]
        else:
            cards = BingoCard.objects.filter(private=False)
            return cards.order_by('-created_date')[:5]


class ContactView(SuccessMessageMixin, generic.FormView):
    """Contact Page View

    Displays social media links and email form for users to get in touch
    with the developer (me). View should contain the Contact form from
    forms.py and should include the most recent contact info from database.

    Attributes:
        template_name: template to be rendered
        form_class: form that will be rendered
        success_url: where user will be redirected upon successful form
            submission
        success_message: message to be displayed upon successful form
            submission

    Methods:
        get_context_data: add most recent Contact object to context
        get_initial: set initial value for `name` field to authenticated user's
            username if a user is authenticated
        form_valid: override default behavior to use send_email method from
            from forms.py

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-editing/#formview
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.get_initial

    """

    template_name = 'home/contact.html'
    form_class = ContactForm
    success_url = '/contact/'
    success_message = 'Thanks for the Email!'

    def get_context_data(self, **kwargs):
        """
        Get list of info from Contact Model to be passed to template
        """
        context = super(ContactView, self).get_context_data(**kwargs)
        context['contact'] = Contact.objects.latest('contact_date')
        return context

    def get_initial(self):
        """
        Sets initial value for name field to authenticated user's username
        """
        initial = super(ContactView, self).get_initial()

        if self.request.user.is_authenticated():
            user = self.request.user
            initial['name'] = user.username

        return initial

    def form_valid(self, form):
        """
        Calls form.send_email() when form is submitted.
        """
        form.send_email()
        return super(ContactView, self).form_valid(form)


class AboutView(generic.TemplateView):
    """View for About Page.

    Attributes:
        template_name: template to render

    References:
        * https://docs.djangoproject.com/en/1.11/topics/class-based-views/generic-display/

    """

    template_name = 'home/about.html'
