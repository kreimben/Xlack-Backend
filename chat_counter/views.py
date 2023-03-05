from django.http import JsonResponse
from drf_yasg.openapi import TYPE_BOOLEAN, TYPE_NUMBER, TYPE_OBJECT, TYPE_STRING, Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.request import Request

from .api import CounterApi
from .serializers import ChatCounterSerializer


class CounterView(
    generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView
):
    http_method_names = ["get", "patch"]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return ChatCounterSerializer

    def get(self, request: Request, *args, **kwargs):
        """
        get chat read counter via channel
        """
        channel = self.kwargs.get("channel__hashed_value", None)
        if channel is None:
            return JsonResponse(
                data={"msg": "no channel"}, status=status.HTTP_400_BAD_REQUEST
            )

        api = CounterApi(**kwargs)
        return JsonResponse(api.get_list(**kwargs), safe=False)

    @swagger_auto_schema(
        request_body=Schema(
            type=TYPE_OBJECT,
            properties={
                "most_recent_chat": Schema(
                    type=TYPE_NUMBER, description="id_of_most_recent_chat"
                ),
                "is_reading": Schema(
                    type=TYPE_BOOLEAN, description="is_user_currently_reading?"
                ),
            },
        )
    )
    def patch(self, request: Request, *args, **kwargs):
        """
        update or create chat read counter.
        """
        channel = self.kwargs.get("channel__hashed_value", None)
        if channel is None:
            return JsonResponse(
                data={"msg": "no channel"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = request.user
        if user is None:
            return JsonResponse(
                data={"msg": "no user"}, status=status.HTTP_400_BAD_REQUEST
            )

        api = CounterApi(**kwargs)
        most_recent_chat = request.data.get("most_recent_chat", None)
        is_reading = request.data.get("is_reading", False)
        return JsonResponse(
            api.update(
                chv=channel,
                user=user,
                most_recent_chat=most_recent_chat,
                is_reading=is_reading,
            ),
            safe=False,
        )

    def get_serializer_class(self):
        return ChatCounterSerializer
