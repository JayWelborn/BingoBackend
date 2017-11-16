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


class CardDeleteTests(TestCase):
    """Tests for `card_delete.html`

    Methods:
        setUp: Create card and user
        test_content: Ensure content is present in template

    """

    def setUp(self):
        """
        Create card and user for rendering.
        """

        self.user = User.objects.get_or_create(
            username='templatetest',
            email='test@test.com'
        )[0]
        self.user.set_password('password')
        self.user.save()

        self.profile = UserProfile.objects.get_or_create(
            user=self.user
        )[0]

        self.card = BingoCard.objects.get_or_create(
            title='templatetests',
            creator=self.user
        )[0]

    def test_content(self):
        """
        Ensure card title is present in template
        """

        # Assert response is valid before continuing tests
        self.client.login(username='templatetest', password='password')
        response = self.client.get(
            reverse('cards:card_delete', args=[self.card.pk])
        )
        self.assertEqual(response.status_code, 200)

        # Assert card title rendered in template
        content = response.rendered_content
        self.assertIn(self.card.title, content)


class CardDetailTests(TestCase):
    """Tests for `card_detail.html`

    Methods:
        setUp: Create objects needed to render template
        test_content_present: Card and all Squares should be present in
            rendered template

    References:

    """

    def setUp(self):
        """
        Create objects needed to render template.
        """
        self.user = User.objects.get_or_create(
            username='templatetest',
            email='test@test.com'
        )[0]
        self.user.set_password('password')
        self.user.save()

        self.profile = UserProfile.objects.get_or_create(
            user=self.user
        )[0]

        self.card = BingoCard.objects.get_or_create(
            title='templatetests',
            creator=self.user
        )[0]

        self.squares = []
        for i in range(24):
            square = BingoCardSquare.objects.get_or_create(
                text='square {}'.format(i),
                card=self.card
            )[0]
            self.squares.append(square)

    def test_content_present(self):
        """
        Rendered template should contain Card title, creator's username, and
        text from all cards.
        """

        # Get response and assert page loads
        response = self.client.get(
            reverse('cards:card_detail', args=[self.card.pk])
        )
        self.assertEqual(response.status_code, 200)
        content = response.rendered_content

        # Assert user and card info is rendered
        self.assertIn(self.user.username, content)
        self.assertIn(self.card.title, content)

        # Assert squares are rendered
        for square in self.squares:
            self.assertIn(square.text, content)


class CardListTests(TestCase):
    """Tests for `card_list.html`

    Methods:
        setUp: Create multiple cards for testing
        test_unauthenticated_visitor: Unauthenticated visitors should only see
            public cards listed
        test_authenticated_visitor: Authenticated visitors should see both
            private and public cards

    References:

    """

    def setUp(self):
        """
        Create user and cards for testing.
        """

        self.user = User.objects.get_or_create(
            username='templatetest',
            email='test@test.com'
        )[0]
        self.user.set_password('password')
        self.user.save()

        self.profile = UserProfile.objects.get_or_create(
            user=self.user
        )[0]

        # create public cards
        self.public_cards = []
        for i in range(4):
            card = BingoCard.objects.get_or_create(
                title='public {}'.format(i),
                creator=self.user,
                private=False
            )[0]
            self.public_cards.append(card)

        # create private cards
        self.private_cards = []
        for i in range(4):
            card = BingoCard.objects.get_or_create(
                title='private {}'.format(i),
                creator=self.user,
                private=True
            )[0]
            self.private_cards.append(card)

    def test_unauthenticated_visitor(self):
        """
        Unauthenticated visitors should see only public cards.
        """

        # Make sure no previous test left client logged in
        self.client.logout()

        # Make sure request returns valid response
        response = self.client.get(reverse('cards:card_list'))
        self.assertEqual(response.status_code, 200)
        content = response.rendered_content

        # Assert expected public card info is present
        for card in self.public_cards:
            self.assertIn(card.title, content)
            self.assertIn(card.creator.username, content)

        # Assert private card data is not present
        for card in self.private_cards:
            self.assertNotIn(card.title, content)
            self.assertIn(card.creator.username, content)

    def test_authenticated_visitor(self):
        """
        Authenticated visitors should see both private and public cards.
        """

        self.client.login(username='templatetest', password='password')

        # Make sure request returns valid response
        response = self.client.get(reverse('cards:card_list'))
        self.assertEqual(response.status_code, 200)
        content = response.rendered_content

        # Assert expected public card info is present
        for card in self.public_cards + self.private_cards:
            self.assertIn(card.title, content)
            self.assertIn(card.creator.username, content)


class CardUpdateTests(TestCase):
    """Tests for `card_update.html`

    Methods:
        setUp: Create card for rendering
        test_content: Card and Square data should be included in form.

    """

    def setUp(self):
        """
        Create card for test.
        """

        self.user = User.objets.get_or_create(
            username='testuser',
            email='test@gmail.com'
        )[0]
        self.user.set_password('password')
        self.user.save()

        self.card = BingoCard.objets.get_or_create(
            title='test',
            creator=self.user
        )[0]

        self.squares = []
        for i in range(24):
            square = BingoCardSquare.get_or_create(
                text='square {}'.format(i),
                card=self.card
            )[0]
            self.squares.append(square)

        def test_content(self):
            """
            Form should include current card info in form fields `value`
            attributes.
            """

            # Assert form is rendered without error
            self.client.login(username='testuser', password='password')
            response = self.client.get(
                reverse('cards:card_update', args=[self.card.pk])
            )
            self.assertEqual(response.status_code, 200)

            # Assert card info is included in form's fields
            content = response.rendered_content
            self.assertIn(
                'value="{}"'.format(self.card.title),
                content
            )

            # Assert square info is included in form's fields
            for square in self.squares:
                self.assertIn(
                    'value="{}"'.format(square.text),
                    content
                )
