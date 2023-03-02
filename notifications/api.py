from typing import Dict, List

from chat.models import Chat
from chat_channel.models import ChatChannel

from .models import Notification


def notify_via_signal(chat: Chat = None):
    """
    create notification via signal triggered by saving chat
    """
    sender = chat.chatter
    channel = chat.channel
    members = list(chat.channel.members.all())

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


def notify_via_rest(sender, chat_id, channel_hashed_value):
    """
    test method for POST
    """
    if chat_id == None:
        channel = ChatChannel.objects.prefetch_related("members").get(
            hashed_value__exact=channel_hashed_value
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
                        chat=None,
                        had_read=False,
                    )
                )

        return Notification.objects.save_group(result)
    else:
        c = (
            Chat.objects.select_related("chatter", "channel")
            .prefetch_related("channel__members")
            .get(id=chat_id)
        )
        return len(notify_via_signal(chat=c))


def get_notification_list(receiver) -> List[Dict]:
    """
    get notifications belongs to user
    """

    return Parser.get_via_receiver(receiver)


def read_notification_list(receiver, sender=None, channel=None):
    """
    find notifications and set them to had read
    """

    Parser.read_notification_list(receiver=receiver, sender=sender, channel=channel)
