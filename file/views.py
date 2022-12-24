from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser

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

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
