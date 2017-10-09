from django.views import generic as g

from .models import BingoCard

# Create your views here.
class CardListView(g.ListView):
    """View that displays a list of cards.

    Attributes:
        model: Model to list
        context_object_name: Name used in template for readability
        queryset: Sort list of cards by most recent first

    Methods:

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-display/#listview

    """

    model = BingoCard
    context_object_name = 'bingocards'
    queryset = BingoCard.objects.order_by('-created_date')
    template_name = 'cards/card_list.html'
