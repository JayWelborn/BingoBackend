from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from auth_extension.models import UserProfile
from cards.models import BingoCard, BingoCardSquare
from home.models import Contact

from .serializers import (ContactSerializer, BingoCardSerializer,
                          UserSerializer, BingoCardSquareSerializer,
                          UserProfileSerializer)
from .permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'cards': reverse('card-list', request=request, format=format),
        'contact': reverse('contact-list', request=request, format=format),
    })


class UserList(generics.ListAPIView):
    """
    List Users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    View detailed info about User.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileList(generics.ListAPIView):
    """
    List view for Profiles
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail view for profiles
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class BingoCardList(generics.ListCreateAPIView):
    """
    List all Bingo Cards, or create new Bingo Cards.
    """

    queryset = BingoCard.objects.all()
    serializer_class = BingoCardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class BingoCardDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a Bingo Card.
    """

    queryset = BingoCard.objects.all()
    serializer_class = BingoCardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class BingoCardSquareList(generics.ListCreateAPIView):
    """
    List all Bingo Cards, or create new Bingo Cards Square.
    """

    queryset = BingoCardSquare.objects.all()
    serializer_class = BingoCardSquareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class BingoCardSquareDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a Bingo Card Square.
    """

    queryset = BingoCardSquare.objects.all()
    serializer_class = BingoCardSquareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ContactList(generics.ListCreateAPIView):
    """
    List all contact objects, or create a new contact object.
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a contact object.
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
