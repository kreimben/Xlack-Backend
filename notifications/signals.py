from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from chat.models import Chat
from notifications import api
from notifications.models import Notification


def load_signal():
    print("notifications signals loaded!")


@receiver(post_save, sender=Chat)
def create_notifications(sender, **kwargs):
    """
    Create notifications after chat models had saved
    """
    chat: Chat = kwargs.get("instance", None)
    response: list[Notification] = api.notify(chat=chat)
    channel_layer = get_channel_layer()
    for noti in response:
        noti: Notification
        async_to_sync(channel_layer.group_send)(
            f"{noti.receiver_id}",
            {
                "type": "notifications.broadcast",
                "user_id": noti.receiver_id,
                "recent_chat_id": chat.id,
            },
        )
