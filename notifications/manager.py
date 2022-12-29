# notifications/manager.py

from django.db.models import Manager
from django.db.models import Q


class NotificationManger(Manager):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def save_group(self, model_list: list()):
        """
        save notifications with bulk
        """
        return self.bulk_create(model_list)

    def get_by_recevier(self, receiver):
        """
        return notifications belongs to one receiver,
        which aren't read
        """
        if type(receiver) == int:
            return self.filter(Q(receiver_id=receiver), Q(had_read=False))
        else:
            return self.filter(Q(receiver=receiver), Q(had_read=False))

    def get_by_source(self, **kwargs):
        """
        get notifications belongs to one receiver,
        by source, (sender(if dm) or channel(if not a dm))
        """
        sender = kwargs.get("sender", None)
        channel = kwargs.get("channel", None)
        receiver = kwargs.get("receiver", None)

        if channel != None:  # not a dm
            if type(channel) == str:
                return self.get_by_recevier(receiver).filter(
                    Q(channel__hashed_value=channel)
                )
            return self.get_by_recevier(receiver).filter(Q(channel=channel))
        else:  # find dm
            if type(sender) == int:
                return self.get_by_recevier(receiver).filter(
                    Q(sender_id=sender), Q(channel=None)
                )
            return self.get_by_recevier(receiver).filter(
                Q(sender=sender), Q(channel=None)
            )

    def read_group(self, **kwargs):
        """
        update notifications belongs to one receiver,
        by sender and channel, to `had_read=True`
        """
        return self.get_by_source(**kwargs).update(had_read=True)
