from notifications.models import Notification
from notifications.parser import Parser


def notify(sender, channel=None):
    """
    create notification
    """
    Notification.objects.save_group(Parser.creation(sender=sender, channel=channel))


def create_notification_list(receiver) -> list(dict()):
    """
    get notifications
    """

    sources = Parser.sources(receiver)

    result = list()

    for entry in sources:
        if entry.channel == None:
            result.append(
                dm=entry.sender, count=Notification.objects.get_by_source(entry).Count()
            )
        else:
            result.append(
                channel=entry.channel,
                count=Notification.objects.get_by_source(entry).Count(),
            )

    return result


def read(receiver, sender, channel):

    Notification.objects.read_group(receiver=receiver, sender=sender, channel=channel)
