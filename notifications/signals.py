from django.db.models.signals import post_save
from django.dispatch import receiver

from chat.models import Chat

from notifications import api


def load_signal():
    print("notifications signals loaded!")


@receiver(post_save, sender=Chat)
def create_notifications(sender: Chat, **kwargs):
    """
    Create notifications after chat models had saved
    """
    chat: Chat = kwargs.get("instance", None)

    response = api.notify(chat.chatter, chat.channel)
