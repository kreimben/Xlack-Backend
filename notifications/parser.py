# notifications/parser.py

from chat_channel.models import ChatChannel
from notifications.models import Notification
from custom_user.models import CustomUser
from django.db.models import Q


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

        if type(sender) == int:
            sender = CustomUser.objects.get(id=sender)
        if type(receiver) == int:
            receiver = CustomUser.objects.get(id=receiver)
        if type(channel) == int:
            channel = ChatChannel.objects.get(id=channel)

        _is_dm = True if channel == None else False

        if _is_dm:  # if it's dm, just save
            return Notification.objects.create(
                sender=sender, receiver=receiver, channel=None, had_read=False
            )

        id_of_members = channel.members_id

        result = list()
        for member_id in id_of_members:
            if member_id != sender.id:
                result.append(
                    Notification(
                        sender=sender,
                        receiver=CustomUser.objects.get(id=member_id),
                        channel=channel,
                        had_read=False,
                    )
                )

        return Notification.objects.save_group(result)

    def get_via_receiver(receiver) -> list(dict()):
        """
        create notification sources via receiver
        """
        if type(receiver) == int:
            _receiver = CustomUser.objects.get(id=receiver)
        else:
            _receiver = receiver

        channel_list = list(  # list of channel's id
            Notification.objects.filter(
                Q(had_read=False), Q(receiver=_receiver), ~Q(channel=None)
            )
            .values_list("channel", flat=True)
            .distinct()
        )
        sender_list = list(  # list of sender's id
            Notification.objects.filter(
                Q(had_read=False), Q(receiver=_receiver), Q(channel=None)
            )
            .values_list("sender", flat=True)
            .distinct()
        )

        result = list()
        for channel_id in channel_list:
            result.append(
                dict(
                    channel=channel_id,
                    count=Notification.objects.filter(
                        Q(had_read=False),
                        Q(receiver=_receiver),
                        Q(channel_id=channel_id),
                    ).count(),
                )
            )

        for sender_id in sender_list:
            result.append(
                dict(
                    dm=sender_id,
                    count=Notification.objects.filter(
                        Q(had_read=False),
                        Q(receiver=_receiver),
                        Q(channel=None),
                        Q(sender_id=sender_id),
                    ).count(),
                )
            )

        return result

    def read_notification_list(**kwargs):

        return Notification.objects.read_group(**kwargs)
