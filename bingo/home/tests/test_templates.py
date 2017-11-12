from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from datetime import timedelta

from django.utils import timezone

from auth_extension.models import UserProfile
from cards.models import BingoCard
from home.models import Contact


class BaseTemplateTests(TestCase):
    """Tests for Base Template.

    Methods:
        setUp: Create test User, Profile and Contact objects
        test_template_used: base.html should be used for every view
        test_navbar_links: If user is logged in, navbar should have
            `Search Cards` and `Logout` links. Else, `Login` and `Register`
        test_profile_card: If user is logged in, their profile should be
            previewed on the profile side-bar. Else, no sidebar.
        test_footer: Social links in footer should have links matching latest
            contact object.

    References:

    """

    def setUp(self):
        """
        Create user, Profile, and Contact objects. Create url list.
        """

        self.user = User.objects.get_or_create(
            username='templatetests',
            email='test_templates@gmail.com'
        )[0]
        self.user.set_password('templ@tet3$t$')
        self.user.save()

        self.profile = UserProfile.objects.get_or_create(
            user=self.user,
            website='www.google.com'
        )[0]

        self.contact = Contact.objects.get_or_create(
            title='title2',
            facebook='https://www.facebook.com/jaywelb',
            github='//www.github.com/jaywelborn',
            linkedin='//www.linkedin.com/--jaywelborn--',
            twitter='//www.twitter.com/__jaywelborn__',
            email='jesse.welborn@gmail.com',
            contact_date=timezone.now().date(),
        )[0]

        self.urls = [
            'home:index',
            'home:about',
            'home:contact',
            'auth_extension:unauthorized',
            'auth_extension:permission_denied',
            'cards:card_create',
            'cards:card_list',
        ]

        self.unauth_urls = self.urls
        self.unauth_urls.pop(-1)
        self.unauth_urls.pop(-1)

    def test_template_used(self):
        """
        base.html should be used for all urls.
        """

        self.client.login(
            username='templatetests',
            password='templ@tet3$t$'
        )

        # Ensure user is logged in
        self.assertIn('_auth_user_id', self.client.session)

        for url in self.urls:
            response = self.client.get(reverse(url))
            self.assertTemplateUsed(response, 'base.html')

        self.client.logout()

    def test_navbar_links(self):
        """
        If user is logged in, navbar should have `Search Cards` and `Logout`
        links. Else, `Login` and `Register`
        """

        self.client.login(
            username='templatetests',
            password='templ@tet3$t$'
        )

        for url in self.urls:
            response = self.client.get(reverse(url))
            self.assertIn('Search Cards', response.rendered_content)
            self.assertIn('Logout', response.rendered_content)

        self.client.logout()

        for url in self.unauth_urls:
            response = self.client.get(reverse(url))
            self.assertIn('Login', response.rendered_content)
            self.assertIn('Register', response.rendered_content)

    def test_profile_card(self):
        """
        Profile card should display only when user is logged in.
        """

        self.client.login(
            username='templatetests',
            password='templ@tet3$t$'
        )

        for url in self.urls:
            response = self.client.get(reverse(url))
            self.assertIn(
                'aside class="profile-sidebar',
                response.rendered_content
            )
            self.assertIn(
                self.user.username,
                response.rendered_content
            )
            self.assertIn(
                'My Cards',
                response.rendered_content
            )
            self.assertIn(
                'Edit Profile',
                response.rendered_content
            )
            self.assertIn(
                'New Card',
                response.rendered_content
            )

        self.client.logout()

        for url in self.unauth_urls:
            response = self.client.get(reverse(url))
            self.assertNotIn(
                'aside class="profile-sidebar',
                response.rendered_content
            )

    def test_footer(self):
        """
        Footer social links should match latest contact object.
        """

        for url in self.unauth_urls:
            response = self.client.get(reverse(url))
            content = response.rendered_content
            self.assertIn(self.contact.facebook, content)
            self.assertIn(self.contact.github, content)
            self.assertIn(self.contact.linkedin, content)
            self.assertIn(self.contact.twitter, content)


class IndexTemplateTests(TestCase):
    """Tests for `index.html` template.

    Methods:
        setUp: Create User, and Profile objects.
        test_call_to_action: If logged in, CTA should display
            `Create Bingo Card` else `Login` and `Register`.
        test_card_list: Card-List should contain most recent cards, or
            `No Cards` display if there are no cards.

    """

    def setUp(self):
        """
        Create User and UserProfile objects.
        """

        self.user = User.objects.get_or_create(
            username='indextests',
            email='index@gmail.com'
        )[0]
        self.user.set_password('password')
        self.user.save()

        self.profile = UserProfile.objects.get_or_create(
            user=self.user
        )[0]

    def test_call_to_action(self):
        """
        If logged in, CTA should display `Create Bingo Card` else `Login` and
        `Register`.
        """

        content = self.client.get(reverse('home:index')).rendered_content
        self.assertIn(
            '<a class="call-to-action" href="/accounts/login/">Log In</a>',
            content
        )
        self.assertIn(
            '<a class="call-to-action" href="/accounts/register/">Sign Up</a>',
            content
        )

        self.client.login(
            username='indextests',
            password='password'
        )
        self.assertIn('_auth_user_id', self.client.session)

        content = self.client.get(reverse('home:index')).rendered_content
        self.assertIn(
            'href="/cards/create/">Create a Bingo Card</a>',
            content
        )

    def test_card_list(self):
        """
        Card-List should contain most recent cards, or `No Cards` display if
        there are no cards.
        """
        content = self.client.get(reverse('home:index')).rendered_content
        self.assertIn('<h5>No Bingo Cards yet.</h5>', content)

        for i in range(6):
            BingoCard.objects.create(
                title='card {}'.format(i),
                creator=self.user,
                created_date=timezone.now() - timedelta(days=i)
            )

        # Make sure 5 most recent cards are rendered
        content = self.client.get(reverse('home:index')).rendered_content
        cards = BingoCard.objects.all().order_by('-created_date')
        self.assertEqual(len(cards), 6)
        for i in range(5):
            self.assertIn(cards[i].title, content)

        # Oldest card should not be rendered
        self.assertNotIn(cards[5].title, content)


class ContactTemplateTests(TestCase):
    """ Test `contact.html`.

    Methods:
        setUp: Create Contact object
        test_social_links: Social links should be populated by contact object

    References:

    """

    def setUp(self):
        """
        Create Contact object.
        """

        self.contact = Contact.objects.get_or_create(
            title='contacttests',
            facebook='testbook.com',
            github='testhub.com',
            linkedin='testlink.com',
            twitter='tester.com'
        )[0]

    def test_social_links(self):
        """
        Social links should match contact object.
        """

        content = self.client.get(reverse('home:contact')).rendered_content

        self.assertIn(self.contact.title, content)
        self.assertIn(self.contact.facebook, content)
        self.assertIn(self.contact.github, content)
        self.assertIn(self.contact.linkedin, content)
        self.assertIn(self.contact.twitter, content)


class AboutTemplateTests(TestCase):
    """Test About Template Tests.

    Methods:
        test_content: Assure content is rendered correctly.

    """

    def test_content(self):
        """
        Assure content is rendered correctly.
        """

        content = self.client.get(reverse('home:about')).rendered_content
        self.assertIn('Bingo - About', content)
