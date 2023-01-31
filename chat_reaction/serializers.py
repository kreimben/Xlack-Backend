from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from chat_reaction.models import ChatReaction


class Util:
    def to_repr(icon: str):
        rep = icon.encode("ascii").decode("unicode_escape")

        return rep

    def to_inter(icon: str):
        if not isinstance(icon, str):
            msg = 'Incorrect type, expected strng, but got %s'
            raise ValidationError(msg % type(icon))

        code = icon.encode("unicode_escape").decode("ascii")

        return code


class IconField(serializers.Field):

    def to_representation(self, value):
        rep = Util.to_repr(value.icon)

        return rep

    def to_internal_value(self, data):
        code = Util.to_inter(data.icon)

        return code


class ChatReactionSerializer(serializers.ModelSerializer):
    icon = IconField(source='*')
    count = serializers.IntegerField(source='reactors.count', read_only=True)

    class Meta:
        model = ChatReaction
        validators = [
            UniqueTogetherValidator(
                queryset=ChatReaction.objects.all(),
                fields=['chat', 'icon']
            )
        ]
        fields = ['chat_id', 'id', 'icon', 'count', 'reactors']


class ChatReactionListSerializer(serializers.ModelSerializer):
    icon = IconField(source='*')

    class Meta:
        model = ChatReaction
        validators = [
            UniqueTogetherValidator(
                queryset=ChatReaction.objects.all(),
                fields=['chat', 'icon']
            )
        ]
        fields = ['id', 'icon', 'reactors']
