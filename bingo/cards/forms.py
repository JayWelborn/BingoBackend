from django.forms.models import inlineformset_factory
from django import forms

# app imports
from bingo.forms import CrispyBaseModelForm

# relative imports
from .models import BingoCard, BingoCardSquare


class BingoCardForm(CrispyBaseModelForm):
    """Form for Creating BingoCards.

    Fields:
        Meta:
            model: Declares model for ModelForm
            fields: Tuple containing attributes form BingoCard model

    Methods:
        __init__: Give form id, method, and action for crispy rendering.

    References:
        * https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#modelform

    """

    def __init__(self, *args, **kwargs):
        """
        Give form crispy attributes.
        """
        super(BingoCardForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'bingo_card_form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_tag = False

    class Meta:
        model = BingoCard
        fields = ('title', 'free_space', 'creator', 'private')


class BingoSquareForm(CrispyBaseModelForm):
    """Form for creating BingoCardSquares.

    Fields:
        Meta:
            model: declares model for ModelForm

    Methods:
        __init__: add helper attributes for crispy rendering

    References:
        * https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#modelform

    """

    def __init__(self, *args, **kwargs):
        """
        Make form crispy
        """
        super(BingoSquareForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'bingo_square_form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_tag = False

    class Meta:
        model = BingoCardSquare
        exclude = ('created_date',)


# https://docs.djangoproject.com/en/1.11/ref/forms/models/#inlineformset-factory
BingoSquareFormset = inlineformset_factory(
    BingoCard,
    BingoCardSquare,
    form=BingoSquareForm,
    min_num=24,
    max_num=24,
    validate_min=True,
    validate_max=True,
)
