# django imports
from django import forms

# app imports
from bingo.forms import CrispyBaseModelForm
from .models import BingoCard


class BingoCardForm(CrispyBaseModelForm):
    """Form for Creating BingoCards.

    Fields:
        Meta:
            Model: Declares model for ModelForm
            fields: Tuple containing attributes form BingoCard model

    Methods:
        __init__: Give form id, method, and action for crispy rendering.

    References:
        * * https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#modelform

    """

    def __init(self, *args, **kwargs):
        """
        Give form crispy attributes.
        """
        super(BingoCardForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'bingo_card_form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'

    class Meta:
        model = BingoCard
        fields = ('title', 'free_space', 'creator', 'private')
