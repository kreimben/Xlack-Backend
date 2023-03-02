from django.db import models
from django.db.models import Prefetch

from chat_channel.models import ChatChannel

from .models import Counter


class CounterApi:
    counter = Counter.objects.all()
    chv = None

    def __init__(self, **kwargs):
        chv = kwargs.get("channel__hashed_value", None)
        if chv:
            self.chv = chv

    def __get_counter_list(self, **kwargs):
        if self.chv is None:
            raise ValueError(
                "CounterApi>>__get_counter_list:ERROR, channel is None", self.chv
            )
        else:
            self.counter.filter(channel__hashed_value=self.chv)

    def __update_counter(self, **kwargs):
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
            q = self.counter.get_or_create(channel__hashed_value=self.chv, user=user)
            q.update(most_recent_chat_id=most_recent_chat, is_reading=is_reading)
            return q

    def get_list(self, **kwargs):
        """
        Get or create counter which depends on chat channel,
        and return instance of it
        """
        qs = self.__get_counter_list(**kwargs)
        if qs == None:
            return {
                "all": ChatChannel.objects.get(hashed_value=self.chv).members.count()
            }
        member_count = qs.channel.members.count()
        reading = qs.filter(is_reading=True).count()
        num = member_count - reading
        dic = {}
        for counter in qs:
            dic[counter.most_recent_chat.id] = num
            num = num - 1
        return dic

    def update(self, **kwargs):
        """
        Update single counter's read info data
        required : kwargs['user']
                   kwargs['most_recent_chat']
        """
        q = self.__update_counter(**kwargs)
        return q
