from notifications.models import Notification
from notifications.parser import Parser


def notify(sender, channel=None):
    """
    create notification with provided `sender`,`channel`
    find where the sender belongs to, and create multiple notifications by receiver
    """
    Notification.objects.save_group(Parser.creation(sender=sender, channel=channel))


def create_notification_list(receiver) -> list(dict()):
    """
    get notifications belongs to user
    """

    sources = Parser.sources(receiver)

    result = list()

    for entry in sources:
        if entry.channel == None:
            result.append(
                dm=entry.sender, count=Notification.objects.get_by_source(entry).count()
            )
        else:
            result.append(
                channel=entry.channel,
                count=Notification.objects.get_by_source(entry).count(),
            )

    return result


def read(receiver, sender, channel):
    """
    find notifications and set them to had read
    """

    Notification.objects.read_group(receiver=receiver, sender=sender, channel=channel)
