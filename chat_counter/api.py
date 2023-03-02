from django.db import models
from django.db.models import Prefetch

from .models import Counter, ReadInfo
from .serializers import ChatCounterSerializer


class CounterApi:
    user = Null
    channel = Null
    most_recent_chat = Null
    queryset = Counter.objects.all()

    def __get_queryset(self):
        chv = self.kwargs.get("channel__hashed_value", None)
        user = self.kwargs.get("user", None)
        if chv is None:
            raise ValueError("CounterApi>>__get_queryset:ERROR, channel is None", chv)
        else:
            return (
                self.queryset.select_related("channel")
                .filter(channel__hashed_value__exact=chv)
                .prefetch_related(
                    Prefetch(
                        "readinfo",
                        queryset=ReadInfo.objects.filter(
                            most_recent_chat__channel__hashed_value__exact=chv,
                            counter__channel__hashed__value__exact=chv,
                        ),
                    )
                )
            )

    def get(self, channel):
        """
        Get or create counter which depends on chat channel,
        and return instance of it
        """
        Counter.objects.get_or_create(channel=channel)

        pass

    def update(self, channel, user, chat):
        """
        Update counter's read info data
        """
        pass
