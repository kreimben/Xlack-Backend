# notifications/manager.py
from django.db.models import Manager
from django.db.models import Q

# TODO: optimize, manage exceptions


class NotificationManger(Manager):
    def get_by_recevier(self, **kwargs):
        """
        return notifications belongs to one receiver,
        which aren't read
        """

        receiver = kwargs.get("receiver", None)

        # prefetching would be better?

        return self.filter(Q(receiver=receiver), Q(had_read=False))

    def get_by_source(self, **kwargs):
        """
        get notifications belongs to one receiver,
        by source, (sender and channel)
        """
        sender = kwargs.get("sender", None)
        channel = kwargs.get("channel", None)
        return self.get_by_recevier(self, kwargs).filter(
            Q(sender=sender), Q(channel=channel)
        )

    def read_group(self, **kwargs):
        """
        update notifications belongs to one receiver,
        by sender and channel, to `had_read=True`
        """
        return self.get_by_source(kwargs).update(had_read=True)

    def save_group(self, **kwargs):
        """
        save notifications with bulk
        """
        return self.bulk_create(kwargs)
