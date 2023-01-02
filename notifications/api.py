from typing import Dict, List

from chat.models import Chat
from notifications.parser import Parser


def notify(chat: Chat = None):
    """
    create notification with provided `sender`,`channel`
    find where the sender belongs to, and create multiple notifications by receiver
    """

    return Parser.create_via_sender(
        sender_id=chat.chatter.id, chat=chat, channel_hashed_value=chat.channel.hashed_value
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
