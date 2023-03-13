from django.db.models import Q, Prefetch

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
    test method via POST
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

        return len(Notification.objects.save_group(result))
    else:
        c = (
            Chat.objects.select_related("chatter", "channel")
            .prefetch_related("channel__members")
            .get(id=chat_id)
        )
        return len(notify_via_signal(chat=c))


def get_notification_list(receiver) -> dict[str, dict[str, int]]:
    """
    get notifications belongs to user
    """

    notifications = Notification.objects. \
        select_related("channel", "receiver"). \
        filter(Q(had_read=False) & Q(receiver=receiver)). \
        prefetch_related(Prefetch('channel', queryset=ChatChannel.objects.select_related('workspace')))

    # For explanation of below codes,
    # This is for O(1) time complexity of dictionary computation
    # and O(n) time complexity of array computation (n is number of key in `d`.)
    d = {}
    for notification in notifications:
        # notification: Notification  # For debugging
        hv = notification.channel.hashed_value
        if d.get(hv):
            d[hv]['count'] += 1
        else:
            d[hv] = {'channel_hashed_value': notification.channel.hashed_value,
                     'workspace_hashed_value': notification.channel.workspace.hashed_value,
                     'count': 1}  # workspace hashed value and it's count.
    res = []
    for _, v in d.items():
        res.append(v)
    return res


def read_notification_list(receiver=None, channel=None):
    """
    find notifications and set them to had read
    """
    noti = (
        Notification.objects.select_related("channel", "receiver")
        .filter(
            Q(had_read=False) & Q(receiver=receiver) & Q(channel__hashed_value=channel)
        )
        .update(had_read=True)
    )
    return noti
