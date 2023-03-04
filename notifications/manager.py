# notifications/manager.py

from django.db.models import Manager, Q


class NotificationManger(Manager):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def save_group(self, model_list: list()):
        """
        save notifications with bulk
        """
        return self.bulk_create(model_list)
