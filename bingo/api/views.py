from rest_framework import generics

from home.models import Contact

from .serializers import ContactSerializer


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
