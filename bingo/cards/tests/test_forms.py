from django.contrib.auth.models import User
from django.test import TestCase

from cards.forms import BingoCardForm, BingoSquareForm, BingoSquareFormset
from cards.models import BingoCard, BingoCardSquare


class BingoCardFormTests(TestCase):
    """Tests for BingoCardForm

    Methods:
        setUp: Create test data for form
        test_helper: Crispy helper should exist and have appropriate attributes
        test_form_accepts_valid_data: Form should accept valid data
        test_card_created_correctly: New BingoCard should be created with data
            from form, and defaults for attributes not included in the form.
        test_form_rejects_invalid_data: Form should only be valid if all
            required fields are present.

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
            'creator': str(self.user.id),
            'private': False
        }

    def test_helper(self):
        """
        Form should get crispy helper attributes when instantiated.
        """

        form = BingoCardForm()

        self.assertTrue(form.helper)
        self.assertEqual(form.helper.form_id, 'bingo_card_form')
        self.assertEqual(form.helper.form_method, 'post')
        self.assertEqual(form.helper.form_action, '.')

    def test_form_accepts_valid_data(self):
        """
        Form should accept and process valid data.
        """
        form = BingoCardForm(self.data)

        self.assertTrue(form.is_valid())

    def test_card_created_correctly(self):
        """
        Form should create new BingoCard properly.
        """

        # instantiate form, and save it
        form = BingoCardForm(self.data)
        if form.is_valid():
            test_card = form.save()

        # check card in DB against card returned by form
        card = BingoCard.objects.get(title='FormTestTitle')
        self.assertTrue(card)
        self.assertEqual(card, test_card)
        self.assertEqual(card.creator, self.user)

    def test_form_rejects_incomplete_data(self):
        """
        Form should only be valid if all required fields are present.
        """

        no_title, no_free_space, no_creator = self.data, self.data, self.data
        no_title.pop('title')

        no_free_space.pop('free_space')

        no_creator.pop('creator')

        self.assertFalse(BingoCardForm(no_title).is_valid())
        self.assertFalse(BingoCardForm(no_free_space).is_valid())
        self.assertFalse(BingoCardForm(no_creator).is_valid())


class BingoSquareFormTests(TestCase):
    """Tests for BingoSquareForm

    Methods:
        setUp: Create test data for form
        test_helper: Crispy helper should exist and have appropriate attributes
        test_form_accepts_valid_data: Form should accept valid data
        test_card_created_correctly: New BingoSquare should be created with
            data from form, and defaults for attributes not included in the
            form.
        test_form_rejects_incomplete_data: Form should not be valid if fields
            are missing.

    References:
        * http://test-driven-django-development.readthedocs.io/en/latest/05-forms.html

    """

    def setUp(self):
        """
        Create Test data.
        """

        # User to serve as card's creator
        self.user = User.objects.create(
            username='CardSquareTestUser',
            email='squaretest@gmail.com'
        )
        self.user.set_password('squaref0rm!')
        self.user.save()

        self.card = BingoCard.objects.get_or_create(
            title='SquareFormTest',
            creator=self.user,
        )[0]
        self.card.save()

        self.data = {
            'text': 'CardSquareTest',
            'card': str(self.card.id),
        }

    def test_helper(self):
        """
        Form should get crispy helper attributes when instantiated.
        """

        form = BingoSquareForm()

        self.assertTrue(form.helper)
        self.assertEqual(form.helper.form_id, 'bingo_square_form')
        self.assertEqual(form.helper.form_method, 'post')
        self.assertEqual(form.helper.form_action, '.')

    def test_form_accepts_valid_data(self):
        """
        Form should accept and process valid data.
        """
        form = BingoSquareForm(self.data)
        self.assertTrue(form.is_valid())

    def test_square_created_correctly(self):
        """
        Form should create new BingoCard properly.
        """

        # instantiate form, and save it
        form = BingoSquareForm(self.data)
        if form.is_valid():
            test_square = form.save()

        # check card in DB against card returned by form
        square = BingoCardSquare.objects.get(text='CardSquareTest')
        self.assertTrue(square)
        self.assertEqual(square, test_square)
        self.assertEqual(square.card, self.card)
        self.assertEqual(square.card.creator, self.user)

    def test_form_rejects_incomplete_data(self):
        """
        Form should only be valid if all fields are present.
        """

        # Copy data, but remove part
        no_text, no_card = self.data, self.data
        no_text.pop('text')
        no_card.pop('card')

        # Assert form is invalid
        self.assertFalse(BingoSquareForm(no_text).is_valid())
        self.assertFalse(BingoSquareForm(no_card).is_valid())


class BingoSquareFormsetTests(TestCase):
    """Tests for BingoSquareFormset

    Methods
        setUp: Create test data for formset
        test_helper: test that formset can access form's helper
        test_formset_accepts_valid_data: Formset should accept valid data
        test_squares_created_correctly: Formset should create squares all
            associated with a parent card set as formset.instance
        test_formset_rejects_too_many_forms: Formset should require max of
            24 forms
        test_formset_rejects_too_few_forms: Formset should require minimum of
            24 forms

    References:
        * http://schinckel.net/2016/04/30/%28directly%29-testing-django-formsets/
        * http://whoisnicoleharris.com/2015/01/06/implementing-django-formsets.html#test-the-formset
        * https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#inline-formsets
        * https://docs.djangoproject.com/en/1.11/ref/forms/models/#django.forms.models.inlineformset_factory

    """

    def setUp(self):
        """
        Create test data
        """

        # Create user
        self.user = User.objects.get_or_create(
            username='FormsetTestUser',
            email='something@yahoo.org'
        )[0]
        self.user.set_password('bingo')
        self.user.save()

        # Create card
        self.card = BingoCard.objects.get_or_create(
            title='FormsetTest',
            free_space='free_space',
            creator=self.user,
        )[0]

        # Formset data
        self.data = {
            'squares-TOTAL_FORMS': 24,
            'squares-INITIAL_FORMS': 0,
            'squares-MAX_NUM_FORMS': 24,
            'squares-MIN_NUM_FORMS': 24,
        }

        # iteratively add squares to data dict
        for i in range(24):
            text_key = 'squares-{}-text'.format(i)
            text_value = 'square {}'.format(i)
            self.data[text_key] = text_value

    def test_helper(self):
        """
        Formset forms should have crispy helper
        """

        formset = BingoSquareFormset()
        for form in formset.forms:
            helper = form.helper
            self.assertTrue(helper)
            self.assertEqual(helper.form_id, 'bingo_square_form')
            self.assertEqual(helper.form_method, 'post')
            self.assertEqual(helper.form_action, '.')

    def test_formset_accepts_valid_data(self):
        """
        Formset should have access to helper for crispy rendering.
        """

        formset = BingoSquareFormset(self.data)
        formset.instance = self.card
        self.assertTrue(formset.is_valid())

    def test_squares_created_correctly(self):
        """
        Formset should create 24 squares related to BingoCard (also created).
        """

        # Create and save formset associated with self.card
        formset = BingoSquareFormset(self.data)
        formset.instance = self.card
        if formset.is_valid():
            formset.save()

        # Check that 24 squares exist, and that all
        # have self.card as their ForeignKey
        squares = BingoCardSquare.objects.filter(card=self.card)
        self.assertEqual(len(squares), 24)
        for square in squares:
            self.assertEqual(square.card, self.card)

        # Clean newly create cards out of database
        squares.delete()
        squares = BingoCardSquare.objects.all()

        self.assertEqual(len(squares), 0)

    def test_formset_rejects_too_many_forms(self):
        """
        Formset should enforce a max of 24 forms per set.
        """

        # Add another item to form data
        test_data = self.data
        test_data['squares-24-text'] = 'square 24'

        # ManagementForm data must match number of forms present
        test_data['squares-TOTAL_FORMS'] = 25

        # data should include 25 forms plus 3 for management form data
        self.assertGreater(len(test_data), 28)

        # Formset with too many dictionary items should be rejected
        formset = BingoSquareFormset(test_data)
        self.assertFalse(formset.is_valid())

    def test_formset_rejects_too_few_forms(self):
        """
        Formset should enforce a minimum of 24 forms per set.
        """

        # pop a form from self.data
        test_data = self.data
        test_data.pop('squares-23-text')
        test_data['squares-TOTAL_FORMS'] = 23

        # formset should be shorter than normal
        self.assertLess(len(test_data), 28)

        # Formset with too few items should be rejected
        formset = BingoSquareFormset(test_data)
        self.assertFalse(formset.is_valid())
