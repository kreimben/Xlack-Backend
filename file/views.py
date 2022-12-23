from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser

from file.models import File
from file.serializers import FileSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
