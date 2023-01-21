from django.db.models.signals import m2m_changed

from chat_channel.models import ChatChannel
from workspace.models import Workspace


def load_chat_channel_signal():
    print('chat_channel signal loaded!')


def adjust(instance: ChatChannel, **kwargs):
    """
    This function is for invite member in chat channels to workspace.
    """
    chat_channel = ChatChannel.objects.get(hashed_value=instance.hashed_value)
    workspace: Workspace = chat_channel.workspace
    workspace.members.clear()
    channels = workspace.chat_channel.all()

    for channel in channels:
        for member in channel.members.all():
            workspace.members.add(member.id)

    workspace.save()


m2m_changed.connect(adjust, sender=ChatChannel.members.through)
