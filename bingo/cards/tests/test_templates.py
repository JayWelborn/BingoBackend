from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from auth_extension.models import UserProfile
from cards.models import BingoCard, BingoCardSquare
from cards.forms import BingoCardForm, BingoSquareForm, BingoSquareFormset


class CardCreateTests(TestCase):
    """Tests for `card_create.html`

    Methods:
        setUp: Create User and Profile instances for login
        test_form_present: BingoCardForm fields should be in rendered content
        test_formset_present: BingoSquareFormset fields should be in rendered
            content

    References:

    """

    def setUp(self):
        """
        Create User and Profile to log in.
        """

        self.user = User.objects.get_or_create(
            username='user',
            email='user@gmail.com'
        )[0]
        self.user.set_password('password')
        self.user.save()

        self.profile = UserProfile.objects.get_or_create(
            user=self.user
        )[0]
        self.profile.save()

        self.client.login(
            username='user',
            password='password'
        )

    def test_form_present(self):
        """
        BingoCardForm should be present in template
        """

        response = self.client.get(reverse('cards:card_create'))
        self.assertEqual(response.status_code, 200)
        content = response.rendered_content
        form = BingoCardForm()

        # Each field from the form should be rendered as an input with name
        # matching the entry in the `fields` tuple in forms.py
        for field in form.fields:
            name = 'name="{}"'.format(field)
            self.assertIn(name, content)

        # Form's id, method, and action should be present in content
        self.assertIn(form.helper.form_id, content)
        self.assertIn(form.helper.form_method, content)
        self.assertIn(form.helper.form_action, content)

    def test_formset_present(self):
        """
        BingoSquareFormset should be present when template rendered.
        """
        response = self.client.get(reverse('cards:card_create'))
        self.assertEqual(response.status_code, 200)
        content = response.rendered_content
        formset = BingoSquareFormset()
        form = BingoSquareForm()

        # Each formset should have an ID and name with the formset's prefix
        # and its instance number
        for i in range(formset.min_num):
            text = ('input type="text" name="squares-{}-text"'.format(i) +
                    ' maxlength="40" class="textinput textInput"' +
                    ' id="id_squares-{}-text"'.format(i))
            self.assertIn(text, content)

        for i in range(formset.max_num):
            text = ('input type="text" name="squares-{}-text"'.format(i) +
                    ' maxlength="40" class="textinput textInput"' +
                    ' id="id_squares-{}-text"'.format(i))
            self.assertIn(text, content)

        self.assertIn(form.helper.form_id, content)
        self.assertIn(form.helper.form_method, content)
        self.assertIn(form.helper.form_action, content)


class CardDetailTests(TestCase):
    """Tests for `card_detail.html`

    Methods:

    References:

    """
