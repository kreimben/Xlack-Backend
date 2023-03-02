from typing import Dict, List

from chat.models import Chat

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

    return Parser.create_via_sender(
        sender_id=chat.chatter.id,
        chat=chat,
        channel_hashed_value=chat.channel.hashed_value,
    )


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
