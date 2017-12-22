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
        read_only_fields: specifies which fields can't be written to via API
        extra_kwargs:
            password: set password so it is write-only. No one should be
                allowed to see any user's password hash

    Methods:
        create: Upon creation, new User should have a blank profile associated
            with it.

    References:
        * http://www.django-rest-framework.org/tutorial/1-serialization/#using-Hyperlinkedmodelserializers

    """

    bingo_cards = serializers.HyperlinkedRelatedField(
        many=True, view_name='bingocard-detail', read_only=True)
    profile = serializers.HyperlinkedRelatedField(
        many=False, view_name='userprofile-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'bingo_cards',
                  'profile', 'email', 'password')
        read_only_fields = ('is_staff', 'is_superuser',
                            'is_active', 'date_joined',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        Create new User object, as well as an associated Profile Object
        with blank fields.
        """

        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'))
        UserProfile.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        """
        Update passwords via `User.set_password` method. Update
        other fields normally.
        """

        if validated_data.get('username'):
            instance.username = validated_data.get('username')

        if validated_data.get('email'):
            instance.email = validated_data.get('email')

        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))

        instance.save()
        return instance


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """Seralizer for User Profiles.

    Fields:
        user: related User object
        model: model to be serialized
        fields: fields to include in serialization

    References:
            * http://www.django-rest-framework.org/tutorial/1-serialization/#using-Hyperlinkedmodelserializers

    """

    user = serializers.HyperlinkedRelatedField(
        many=False, view_name='user-detail', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('url', 'user', 'created_date', 'slug', 'picture',
                  'website', 'about_me')
        extra_kwargs = {
            'slug': {'read_only': True},
        }


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
        fields = ('url', 'id', 'title', 'facebook', 'github',
                  'linkedin', 'twitter', 'email', 'contact_date')


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
        fields = ('id', 'url', 'text', 'card')


class BingoCardSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to convert Bingo Cards to various data types.

    Fields:
        squares: Reverse lookup field to find squares related to a Bingo Card.
        creator:
        model: model to be serialized
        fields: fields to include in serialization

    Methods:
        validate_squares: There should be exactly 24 squares in data to be
            serialized.
        create: Create new Bingo Card and 24 Squares linked to newly created
            card.
        update: Update Bingo Card and update related squares if needed.

    References:
        * http://www.django-rest-framework.org/tutorial/1-serialization/#using-Hyperlinkedmodelserializers

    """

    squares = BingoCardSquareSerializer(many=True, read_only=False)
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = BingoCard
        fields = ('url', 'id', 'title', 'free_space', 'creator', 'squares')

    def validate_squares(self, value):
        """
        Ensure exactly 24 squares are present.
        """
        if len(value) != 24:
            raise serializers.ValidationError('Must have exactly 24 squares')
        return value

    def create(self, validated_data):
        """
        Create Bingo Card with Squares.
        """

        if validated_data.get('free_space'):
            free_space = validated_data.get('free_space')
        else:
            free_space = 'Free Space'

        card = BingoCard.objects.create(
            title=validated_data.get('title'),
            creator=validated_data.get('creator'),
            free_space=free_space
        )
        card.save()

        for square in validated_data.get('squares'):
            new_square = BingoCardSquare.objects.create(
                text=square['text'],
                card=card
            )
            new_square.save()

        return card

    def update(self, instance, validated_data):
        """
        Perform partial updates on Cards and Squares.

        Params:
            self: BingoCardSerializer instance
            instance: BingoCard instance
            validated_data: Data to be updated on model. Can contain any field
                Bingo Card, or updates to some or all squares.

        """

        squares = instance.squares.all()
        new_squares = validated_data['squares']

        # Update fields on instance
        for key, value in validated_data.items():
            if (
                key in dir(instance) and
                validated_data[key] != getattr(instance, key) and
                key != 'squares'
            ):
                setattr(instance, key, value)

        # Update squares
        for index, square in enumerate(squares):
            if square.text != new_squares[index]['text']:
                square.text = new_squares[index]['text']
                square.save()

        instance.save()
        return instance
