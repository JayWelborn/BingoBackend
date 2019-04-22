from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import (APITestCase, APIRequestFactory,
                                 force_authenticate,
                                 )
from rest_framework.views import APIView

from api.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly
from api.viewsets import UserViewset, BingoCardViewset, UserProfileViewset
from cards.models import BingoCard, BingoCardSquare


class PermissionsTestCase(APITestCase):
    """Tests for Custom Permissions Classes.

    Custom API Root should return a response with rest_auth urls added to my
    project urls. This includes the rest auth project URLS in the browsable API,
    to assist in debugging.

    Methods:
        setUp: Generate test data
        tearDown: Empty test database after test completion
        test_is_owner: Ensure is_owner returns true when requester owns object,
            and false when they don't
    """

    def setUp(self):
        """
        Generate test data
        """
        self.url_prefix = 'http://testserver'

        self.user = User.objects.get_or_create(
            username='test',
            email='test@test.testing'
        )[0]
        self.user.set_password('password')
        self.user.save()

        squares = []
        for i in range(24):
            squares.append({'text': 'square {}'.format(i)})

        self.valid_data = {
            'title': 'test title',
            'creator': self.user,
            'squares': squares
        }

        self.card = BingoCard.objects.get_or_create(
            title='self.card',
            creator=self.user)[0]

        for i in range(24):
            BingoCardSquare.objects.get_or_create(
                text='self.card.square {}'.format(i),
                card=self.card
            )[0]

        self.factory = APIRequestFactory()

    def tearDown(self):
        """
        Clean test data.
        """

        for square in BingoCardSquare.objects.all():
            square.delete()

        for card in BingoCard.objects.all():
            card.delete()

        for user in User.objects.all():
            user.delete()

    def test_is_owner(self):
        # Get should return true even for unauthenticated requests
        request = self.factory.get(
            reverse('user-detail', args=[self.user.pk]))
        view_method = UserViewset.as_view({'get': 'list'})
        perm = IsOwnerOrReadOnly()
        self.assertTrue(
            perm.has_object_permission(request, view_method, self.user.profile))

        # Put should return false if the wrong guest is authenticated
        other_user = User.objects.create_user(username="other",
                                              email="other@other.com",
                                              password="otherpassword")
        view = BingoCardViewset.as_view({'put': 'update'})
        request = APIRequestFactory().put(
            reverse('user-detail', args=[self.user.pk]),
            instance=self.user,
            data={'username': 'somethingElse'},
        )
        force_authenticate(request, user=other_user)
        request = APIView().initialize_request(request)

        self.assertFalse(
            perm.has_object_permission(request, view_method, self.card))

    def test_is_user(self):
        """
        Tests for IserUserOrReadOnly permission class.

        has_object_permission should return True if request is a safe method or
        if the object's user attribute is the request user, or if the requesting
        user is staff.

        Should return false if regular user is attempting to access another
        user's profile
        """
        # normal user on self
        view = UserProfileViewset.as_view(
            {'get': 'retrieve', 'patch': 'partial_update'})
        request = self.factory.get(reverse('userprofile-detail',
                                           args=[self.user.profile.pk]))
        force_authenticate(request, user=self.user)
        perm = IsUserOrReadOnly()
        request = APIView().initialize_request(request)
        self.assertTrue(
            perm.has_object_permission(request, view, self.user.profile))

        # super user on other
        superuser = User.objects.create_superuser(
            username="super", email="super@sup.per", password="supersupersuper8"
        )
        request = self.factory.get(
            reverse('userprofile-detail', args=[self.user.profile.pk])
        )
        force_authenticate(request, user=superuser)
        request = APIView().initialize_request(request)
        self.assertTrue(
            perm.has_object_permission(request, view, superuser.profile))

        # normal user on other
