from typing import Dict, List

from notifications.parser import Parser


def notify(sender, chat=None, channel=None, receiver=None):
    """
    create notification with provided `sender`,`channel`
    find where the sender belongs to, and create multiple notifications by receiver

    :param int sender: id of sender
    :param channel: Hashed Value of channel
    :param receiver: id of receiver
    """

    return Parser.create_via_sender(
        sender=sender, chat=chat, channel=channel, receiver=receiver
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
