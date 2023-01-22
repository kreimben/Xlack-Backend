from django.apps import AppConfig


class ChannelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat_channel'

    def ready(self):
        from . import signals
        signals.load_chat_channel_signal()
