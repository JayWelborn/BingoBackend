from django.contrib.auth.models import User
from django.test import TestCase

from cards.forms import BingoCardForm


class BingoCardFormtests(TestCase):
    """Tests for BingoCardForm

    Methods:
        setUp: Create test data for form
        test_helper: Crispy helper should exist and have appropriate attributes
        test_form_accepts_valid_data: Form should accept valid data
        test_card_created_correctly: New BingoCard should be created with data
            from form, and defaults for attributes not included in the form.

    References:

    * http://test-driven-django-development.readthedocs.io/en/latest/05-forms.html

    """

    def setUp(self):
        """
        Create Test data.
        """

        # User to serve as card's creator
        self.user = User.objects.create(
            username='CardFormTestUser',
            email='formtest@gmail.com'
        )
        self.user.set_password('cardf0rm!')
        self.user.save()

        # sample form data
        self.data = {
            'title': 'FormTestTitle',
            'free_space': 'FormTestFreeSpace',
            'creator': self.user,
            'private': False
        }

    def test_helper(self):
        """
        Form should get crispy helper attributes when instantiated.
        """

        form = BingoCardForm()
        self.assertTrue(form.helper)
