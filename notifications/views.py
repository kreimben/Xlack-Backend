import json

from django.http import JsonResponse
from drf_yasg.openapi import TYPE_NUMBER, TYPE_OBJECT, TYPE_STRING, Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.request import Request

from notifications import api
from notifications.serializers import NotificationSerializer


class NotificationView(
    generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView
):
    http_method_names = ["get", "patch", "post"]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        """
        Get Notification list via requesting user
        No argument need
        """
        receiver = request.user
        if receiver is None:
            return JsonResponse(
                data={"msg": "no recevier"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return JsonResponse(api.get_notification_list(receiver), safe=False)

    @swagger_auto_schema(
        request_body=Schema(
            type=TYPE_OBJECT,
            properties={
                "channel": Schema(
                    type=TYPE_STRING, description="hashed_value of channel"
                ),
            },
        )
    )
    def patch(self, request: Request, *args, **kwargs):
        """
        Read Notification list via source, channel_hashed_value
        """

        channel = request.data.get("channel", None)
        if channel == None:
            return JsonResponse(
                data={"msg": "no source (channel)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        l = api.read_notification_list(receiver=request.user, channel=channel)

        return JsonResponse(
            {
                "notifications_has_been_read": l,
            },
            safe=False,
        )

    @swagger_auto_schema(
        request_body=Schema(
            type=TYPE_OBJECT,
            properties={
                "channel": Schema(
                    type=TYPE_STRING, description="hashed_value of channel"
                ),
            },
        )
    )
    def post(self, request: Request, *args, **kwargs):
        """
        Debug use only,
        create notification directly.
        {channel = "hashed_value of channel"}
        """
        channel = request.data.get("channel", None)
        chat_id = request.data.get("chat_id", None)

        if channel == None and chat_id == None:
            return JsonResponse(
                data={"msg": "no sources (channel&chat)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        noti = api.notify_via_rest(request.user, chat_id, channel_hashed_value=channel)

        return JsonResponse(
            data={"msg": "notification created", "notifications created: ": noti},
            safe=False,
        )

    def get_serializer_class(self):
        return NotificationSerializer
