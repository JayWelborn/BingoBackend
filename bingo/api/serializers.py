from rest_framework import serializers

from home.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """Serializer to Create, Update, and Delete Contact objects.

    Fields:
        model: model to be serialized
        fields: fields to include in Serialization

    References:
        * http://www.django-rest-framework.org/tutorial/1-serialization/#using-modelserializers

    """

    class Meta:
        model = Contact
        fields = (
            'id', 'title', 'facebook', 'github',
            'linkedin', 'twitter', 'email',
        )
