from rest_framework import generics, status, permissions
from rest_framework.request import Request
from rest_framework.response import Response

from chat_reaction.serializers import ChatReactionSerializer
from chat_reaction.models import ChatReaction

from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_NUMBER, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema


class ChatReactionView(
    generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView
):
    http_method_names = ["get", "patch", "post"]
    queryset = ChatReaction.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        qs = ChatReaction.objects.all()

        serial = self.get_serializer(qs, many=True)

        return Response(serial.data)

    @swagger_auto_schema(
        request_body=Schema(
            type=TYPE_OBJECT,
            properties={
                "chat_id": Schema(type=TYPE_NUMBER, description="id of chat"),
                "icon": Schema(
                    type=TYPE_STRING, description="icon of reaction"
                ),
            },
        )
    )
    def post(self, request: Request, *args, **kwargs):
        """ Endpoint for creating new reaction or
            adding user to existing reaction
            (Debug use only)
        """

        chat_id = request.data.get("chat_id", None)
        icon = request.data.get("icon", None)
        icon = icon.encode("unicode_escape").decode("ascii")

        reaction, is_created = ChatReaction.objects.get_or_create(
            chat_id=chat_id, icon=icon)

        if request.user not in reaction.reactors.all():
            reaction.reactors.add(request.user)

            serial = self.get_serializer(reaction)

            print(repr(serial.data['icon']))

            return Response(serial.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=Schema(
            type=TYPE_OBJECT, properties={
                "chat_id": Schema(type=TYPE_NUMBER, description="id of chat"),
                "icon": Schema(
                    type=TYPE_STRING, description="icon of reaction"
                ),
            },
        )
    )
    def patch(self, request: Request, *args, **kwargs):
        """ Endpoint for removing user to existing reaction
            (Debug use only)
        """

        chat_id = request.data.get("chat_id", None)
        icon = request.data.get("icon", None)
        icon = icon.encode("unicode_escape").decode("ascii")

        reaction = ChatReaction.objects.get(chat_id=chat_id, icon=icon)

        if request.user not in reaction.reactors.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            reaction.reactors.remove(request.user)
            if reaction.reactors.count() == 0:
                reaction.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                serial = self.get_serializer(reaction)
                return Response(serial.data)

    def get_serializer_class(self):
        return ChatReactionSerializer
