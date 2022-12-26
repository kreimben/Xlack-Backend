# notifications/parser.py

from chat_channel.models import ChatChannel
from notifications.models import Notification


class Parser:
    """
    Parsing arguments
    """

    def creation(**kwargs):
        """
        Parsing argument for
        creation of notifications,
        with provided sender and channel
        """
        sender = kwargs.get("sender", None)
        channel = kwargs.get("channel", None)

        _is_dm = True if channel == None else False

        # TODO:  benchmark two way finding user,
        # From ChatChannels with User , From User with Channel

        if _is_dm:
            return kwargs

        id_of_members = (
            # select related will do better?
            ChatChannel.objects.prefetch_related("members")
            .filter(name=channel)
            .values_list("members", flat=True)
            # the flat options is True so result of qurreyset
            # is just qurreyset <list of id>
        )

        result = list()
        for member_id in id_of_members:
            if member_id != sender:
                result.append(
                    dict(
                        sender=None,
                        receiver=member_id,
                        channel=channel,
                        had_read=False,
                    )
                )

        return result

    def sources(receiver) -> list(dict()):
        """
        create notification sources via receiver
        """
        sources = Notification.objects.filter(receiver=receiver).distinct(
            "sender", "channel"
        )

        result = list()
        for entry in sources:
            result.append(
                dict(receiver=receiver, channel=entry.channel, sender=entry.sender)
            )

        return result
