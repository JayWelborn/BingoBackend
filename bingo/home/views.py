from django.views import generic

from cards.models import BingoCard


# Create your views here.
class IndexView(generic.ListView):
    """ Home Page View.

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
        if self.request.user.is_authenticated:
            return BingoCard.objects.distinct().order_by('-creation_date')[:5]
        else:
            cards = BingoCard.objects.filter(private=False)
            return cards.order_by('-creation_date')[:5]
