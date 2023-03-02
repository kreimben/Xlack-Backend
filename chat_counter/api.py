from django.db import models
from django.db.models import Prefetch

from .models import Counter, ReadInfo
from .serializers import ChatCounterSerializer


class CounterApi:
    counter = Counter.objects.all()
    readinfo = ReadInfo.objects.all()

    def __get_counter(self, **kwargs):
        chv = self.kwargs.get("channel__hashed_value", None)
        if chv is None:
            raise ValueError("CounterApi>>__get_counter:ERROR, channel is None", chv)
        else:
            return (
                self.counter.select_related("channel", "readinfo")
                .filter(channel__hashed_value__exact=chv)
                .prefetch_related(
                    Prefetch(
                        "readinfo",
                        queryset=ReadInfo.objects.select_related(
                            "user", "most_recent_chat"
                        ).filter(
                            most_recent_chat__channel__hashed_value__exact=chv,
                            counter__channel__hashed__value__exact=chv,
                        ),
                    )
                )
            )

    def __get_readinfo(self, **kwargs):
        user = self.kwargs.get("user", None)
        most_recent_chat_before = self.kwargs.get("most_recent_chat_before", None)
        if user is None:
            raise ValueError("CounterApi>>__get_readinfo:ERROR, user is None", user)
        elif most_recent_chat is None:
            raise ValueError(
                "CounterApi>>__get_readinfo:ERROR, most_recent_chat is None",
                most_recent_chat,
            )
        else:
            return (
                self.readinfo.select_related("counter", "most_recent_chat")
                .filter(channel__hashed_value__exact=chv)
                .get_or_create(user=kwargs.get(user))
                )
            )

    def get(self, **kwargs):
        """
        Get or create counter which depends on chat channel,
        and return instance of it
        """
        qs = self.__get_counter(**kwargs)
        return qs

    def update(self, **kwargs):
        """
        Update counter's read info data
        """
        qs = self.__get_readinfo(**kwargs)
        return qs
