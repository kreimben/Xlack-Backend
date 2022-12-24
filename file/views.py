from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser

from chat_channel.models import ChatChannel
from file.models import File
from file.serializers import FileSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        """
        If client request as `list` or method is `DELETE`, Get queryset about themselves,
        If not (just retrieve for download file), Get not filtering queryset.
        """
        if self.kwargs.get('pk', None) and self.request.method == 'GET':
            return self.queryset
        else:
            return self.queryset.filter(uploaded_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        자신이 업로드한 모든 파일에 대해 가져옵니다.
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        파일 업로드만 담당하며, 다른 비지니스 로직과는 아무 상관이 없습니다.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        `id`를 입력해 파일을 다운 받을 수 있게 합니다.
        """
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        자신의 업로드한 파일이 아니면 지울 수 없습니다.
        """
        return super().destroy(request, *args, **kwargs)
