from itertools import chain

from django.db.models import Q, QuerySet, Prefetch
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from chat.models import Chat
from chat.serializers import ChatSerializer
from chat_reaction.models import ChatReaction
from custom_user.models import CustomUser
from custom_user.serializers import CustomUserSerializer
from file.models import File
from file.serializers import FileSerializer
from search.serializers import SearchSerializer


class SearchView(generics.ListAPIView):
    """
    검색 범위는 3가지로 제한 됨. (추가적으로 필요하면 건의할 것.)
    (링크: https://github.com/Team-Discipline/Xlack-Backend/issues/96)
    1. 채팅 내역
    2. 파일 (이름)
    3. (워크 스페이스 내) 가입자
        3.1. display name
        3.2. title
        3.3. phone number

    response에 chat이 들어갈 수도, 정보가 들어갈 수도, 가입자 정보가 들어갈 수도 있지만,
    response로 배열을 주고 그 안에 하나의 값만 들어감.

    예) 채팅 1개 파일 2개가 검색 결과로 나온다면 크기가 3인 배열이 return되고,
    chat정보 하나 file정보 2개가 각각의 element로 들어가있는 배열을 보내준다.
    """

    serializer_class = SearchSerializer

    def get_queryset(self) -> QuerySet | None:
        kw = self.kwargs.get('search_keyword', '')
        if kw:
            chat = Chat.objects.select_related('file', 'chatter', 'channel') \
                .filter(message__icontains=kw) \
                .prefetch_related(Prefetch('reaction',
                                           queryset=ChatReaction.objects.select_related('chat').all() \
                                           .prefetch_related('reactors')))
            file = File.objects.select_related('uploaded_by').filter(file_name__icontains=kw)
            user = CustomUser.objects.filter(
                Q(display_name__icontains=kw) | Q(title__icontains=kw) | Q(phone_number__icontains=kw)
            )
            res = chain(chat, file, user)
            return list(res)

    def list(self, request: Request, *args, **kwargs):
        q = self.get_queryset()
        data = []

        for i, query in enumerate(q):
            temp = {}
            if isinstance(query, Chat):
                temp['type'] = 'chat'
                temp['chat'] = ChatSerializer(query).data
            elif isinstance(query, File):
                temp['type'] = 'file'
                temp['file'] = FileSerializer(query).data
            elif isinstance(query, CustomUser):
                temp['type'] = 'user'
                temp['user'] = CustomUserSerializer(query).data
            data.append(temp)

        return Response(data)
