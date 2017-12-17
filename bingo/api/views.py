from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
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


class UserViewset(viewsets.ReadOnlyModelViewSet):
    """
    Read only viewset class for User objects.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileViewset(viewsets.ModelViewSet):
    """
    Viewset for User Profiles.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class BingoCardViewset(viewsets.ModelViewSet):
    """
    Viewset for Bingo Cards.
    """

    queryset = BingoCard.objects.all()
    serializer_class = BingoCardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


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


class ContactViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Contact Objects.
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
