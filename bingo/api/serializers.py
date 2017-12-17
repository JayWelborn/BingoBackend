from django.contrib.auth.models import User

from rest_framework import serializers

from auth_extension.models import UserProfile
from cards.models import BingoCard, BingoCardSquare
from home.models import Contact

import pdb


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to convert Users to various data types.

    Fields:
        cards: Reverse lookup field to find Bingo Cards related to a
               given user.
        profile: User's profile data
        model: model to be serialized
        fields: fields to include in serialization

    References:
        * http://www.django-rest-framework.org/tutorial/1-serialization/#using-Hyperlinkedmodelserializers

    """

    bingo_cards = serializers.HyperlinkedRelatedField(
        many=True, view_name='card-detail', read_only=True)
    profile = serializers.HyperlinkedRelatedField(
        many=False, view_name='profile-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'bingo_cards', 'profile',)


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """Seralizer for User Profiles.

    Fields:

    References:
            * http://www.django-rest-framework.org/tutorial/1-serialization/#using-Hyperlinkedmodelserializers

    """

    user = serializers.HyperlinkedRelatedField(
        many=False, view_name='user-detail', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'created_date', 'slug', 'picture', 'website',
                  'about_me')


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to convert Contact objects to various data types.

    Fields:
        model: model to be serialized
        fields: fields to include in Serialization

    References:
        * http://www.django-rest-framework.org/tutorial/1-serialization/#using-Hyperlinkedmodelserializers

    """

    class Meta:
        model = Contact
        fields = ('id', 'title', 'facebook', 'github',
                  'linkedin', 'twitter', 'email',)


class BingoCardSquareSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Bingo Card Squares.

    Fields:
        card: related Bingo Card object
        model: model to be serialized
        fields: fields to include in serialization

    References:
        * http://www.django-rest-framework.org/tutorial/1-serialization/#using-Hyperlinkedmodelserializers

    """

    card = serializers.ReadOnlyField(source='card.title')

    class Meta:
        model = BingoCardSquare
        fields = ('text', 'card')


class BingoCardSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to convert Bingo Cards to various data types.

    Fields:
        squares: Reverse lookup field to find squares related to a Bingo Card.
        creator:
        model: model to be serializers
        fields: fields to include in serialization

    Methods:
        validate_squares: There should be exactly 24 squares in data to be
            serialized.

    References:
        * http://www.django-rest-framework.org/tutorial/1-serialization/#using-Hyperlinkedmodelserializers

    """

    squares = BingoCardSquareSerializer(many=True, read_only=False)
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = BingoCard
        fields = ('id', 'title', 'free_space', 'creator', 'squares')

    def validate_squares(self, value):
        """
        Ensure exactly 24 squares are present.
        """
        pdb.set_trace()
        if len(value) != 24:
            raise serializers.ValidationError('Must have exactly 24 squares')
        return value
