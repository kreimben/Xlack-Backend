from django.db import models
from django.db.models import Count, Prefetch, Q

from chat_channel.models import ChatChannel

from .models import Counter


class CounterApi:
    counter = Counter.objects.all()
    chv = None

    def __init__(self, **kwargs):
        chv = kwargs.get("channel__hashed_value", None)
        if chv:
            self.chv = chv

    def get_list(self, **kwargs):
        """
        Get or create counter which depends on chat channel,
        and return instance of it

        """

        if not self.chv:
            chv = kwargs.get("channel__hashed_value", None)

        reading = self.counter.filter(channel__hashed_value=self.chv, is_reading=True)
        not_reading = self.counter.filter(
            channel__hashed_value=self.chv, is_reading=False
        )

        counters = list(
            ChatChannel.objects.filter(hashed_value=self.chv)
            .values("counter__most_recent_chat_id")
            .annotate(total=Count("members", distinct=True))
            .annotate(
                reading=Count(
                    "counter",
                    filter=Q(counter__is_reading=True),
                    distinct=True,
                )
            )
            .annotate(
                not_reading=Count(
                    "counter",
                    filter=Q(
                        counter__is_reading=False,
                    ),
                    distinct=True,
                )
            )
        )

        total = counters[0]["total"]
        if counters[0]["counter__most_recent_chat_id"] == None:
            return {"all": total}

        for counter in counters:
            total -= counter["reading"]

        l = list()
        for counter in counters:
            total -= counter["not_reading"]
            l.append({counter["counter__most_recent_chat_id"]: total})

        return l

    def update(self, **kwargs):
        """
        Update single counter's read info data
        required : kwargs['user']
                   kwargs['most_recent_chat']
        """

        user = kwargs.get("user", None)
        most_recent_chat = kwargs.get("most_recent_chat", None)
        is_reading = kwargs.get("is_reading", False)
        if self.chv is None:
            raise ValueError(
                "CounterApi>>__get_counter:ERROR, channel is None", self.chv
            )
        elif user is None:
            raise ValueError("CounterApi>>__get_counter:ERROR, user is None", user)
        elif (most_recent_chat is None) and (is_reading is False):
            raise ValueError(
                "CounterApi>>__get_counter:ERROR, most_recent_chat and is_reading are both None",
                most_recent_chat,
                is_reading,
            )
        else:
            self.counter.update_or_create(
                channel__hashed_value=self.chv,
                user=user,
                defaults={
                    "most_recent_chat_id": most_recent_chat,
                    "is_reading": is_reading,
                },
            )
