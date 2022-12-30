# notifications/parser.py
from typing import Dict

from django.db.models import Q, Count

from chat_channel.models import ChatChannel
from custom_user.models import CustomUser
from notifications.models import Notification


class Parser:
    """
    Parsing arguments
    """

    def create_via_sender(*args, **kwargs) -> list():
        """
        Parsing argument for
        creation of notifications,
        with provided sender and channel
        """
        sender = kwargs.get("sender", None)
        channel = kwargs.get("channel", None)
        receiver = kwargs.get("receiver", None)
        chat = kwargs.get("chat", None)

        if type(sender) == int:
            sender = CustomUser.objects.get(id=sender)
        if type(receiver) == int:
            receiver = CustomUser.objects.get(id=receiver)
        if type(channel) == str:
            channel = ChatChannel.objects.get(hashed_value=channel)

        _is_dm = True if channel == None else False

        if _is_dm:  # if it's dm, just save
            return Notification.objects.create(
                sender=sender,
                receiver=receiver,
                channel=None,
                chat=chat,
                had_read=False,
            )

        members = list(channel.members.all())

        result = list()
        for member in members:
            if member != sender:
                result.append(
                    Notification(
                        sender=sender,
                        receiver=member,
                        channel=channel,
                        chat=chat,
                        had_read=False,
                    )
                )

        return Notification.objects.save_group(result)

    def get_via_receiver(receiver) -> [Dict]:
        """
        create notification sources via receiver
        """
        if type(receiver) == int:
            _receiver = CustomUser.objects.get(id=receiver)
        else:
            _receiver = receiver

        channels = list(  # hashed_value list of channel
            Notification.objects.filter(Q(had_read=False) & Q(receiver=_receiver))
            .exclude(Q(channel=None))
            .values_list("channel__hashed_value", flat=True)
            .distinct()
        )


        result = []
        for channel in channels:
            result.append(
                dict(
                    channel_hashed_value=channel,
                    count=Notification.objects.filter(
                        Q(had_read=False)&
                        Q(receiver=_receiver)&
                        Q(channel__hashed_value__exact=channel)
                    ).count()
                )
            )
        return result

    def read_notification_list(**kwargs):
        return Notification.objects.read_group(**kwargs)
