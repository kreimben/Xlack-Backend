from django.apps import AppConfig


class FileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'file'

    def ready(self):
        from . import signals
        signals.load_signal()
