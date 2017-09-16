from django import forms

from crispy_forms.helper import FormHelper


class CrispyBaseForm(forms.Form):
    """Parent Class for app forms to inherit. Sets up a form with FormHelper
    from django_crispy_forms.

    References:
        * http://django-crispy-forms.readthedocs.io/en/latest/form_helper.html#formhelper

    """

    def __init__(self, *args, **kwargs):
        super(CrispyBaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)


class CrispyBaseModelForm(forms.ModelForm):
    """Parent Class for app forms to inherit. Sets up a form with FormHelper
    from django_crispy_forms.

    References:
        * http://django-crispy-forms.readthedocs.io/en/latest/form_helper.html#formhelper

    """

    def __init__(self, *args, **kwargs):
        super(CrispyBaseModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
