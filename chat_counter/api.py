from django.db import models
from django.db.models import Prefetch

from chat_channel.models import ChatChannel

from .models import Counter


class CounterApi:
    counter = Counter.objects.all()
    channel = None | ChatChannel

    def __init__(self, **kwargs):
        chv = kwargs.get("channel__hashed_value", None)
        if chv:
            self.channel = ChatChannel.objects.get(hashed_value=chv)
        else:
            raise ValueError("Couter.__init__>>channel not provided")

    def __get_counter_list(self, **kwargs):
        if self.channel is None:
            raise ValueError(
                "CounterApi>>__get_counter_list:ERROR, channel is None", self.channel
            )
        else:
            return self.counter.filter(channel=self.channel)

    def __update_counter(self, **kwargs):
        user = kwargs.get("user", None)
        most_recent_chat = kwargs.get("most_recent_chat", None)
        is_reading = kwargs.get("is_reading", False)
        if self.channel is None:
            raise ValueError(
                "CounterApi>>__get_counter:ERROR, channel is None", self.channel
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
            q, is_created = self.counter.update_or_create(
                channel=self.channel,
                user=user,
                defaults={
                    "most_recent_chat_id": most_recent_chat,
                    "is_reading": is_reading,
                },
            )
            return repr(q), is_created

    def get_list(self, **kwargs):
        """
        Get or create counter which depends on chat channel,
        and return instance of it
        """
        qs = self.__get_counter_list(**kwargs)
        if qs.count() == 0:
            return {"all": self.channel.members.count()}
        member_count = self.channel.members.count()
        reading = qs.filter(is_reading=True).count()
        not_reading = qs.filter(is_reading=False)
        num = member_count - reading
        dic = {}
        for counter in not_reading:
            num = num - 1
            dic[counter.most_recent_chat.id] = num
        return dic

    def update(self, **kwargs):
        """
        Update single counter's read info data
        required : kwargs['user']
                   kwargs['most_recent_chat']
        """
        q = self.__update_counter(**kwargs)
        return q
