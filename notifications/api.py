from notifications.parser import Parser


def notify(sender, channel=None, receiver=None):
    """
    create notification with provided `sender`,`channel`
    find where the sender belongs to, and create multiple notifications by receiver

    :param int sender: id of sender
    :param channel: id of channel
    :param receiver: id of receiver
    """

    return Parser.create_via_sender(sender=sender, channel=channel, receiver=receiver)


def get_notification_list(receiver) -> list(dict()):
    """
    get notifications belongs to user
    """

    return Parser.get_via_receiver(receiver)


def read_notification_list(receiver, sender=None, channel=None):
    """
    find notifications and set them to had read
    """

    Parser.read_notification_list(receiver=receiver, sender=sender, channel=channel)
