from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from status.models import UserStatus
from status.serializers import UserStatusSerializer
from workspace.models import Workspace


class UserStatusView(ListAPIView):
    queryset = UserStatus.objects.prefetch_related('workspace')
    serializer_class = UserStatusSerializer

    def get_queryset(self, f=None):
        return self.queryset.filter(f)

    def get(self, request: Request, *args, **kwargs):
        workspace_hashed_value = kwargs.get('workspace_hashed_value', None)
        if workspace_hashed_value is None:
            return JsonResponse(data={'msg': 'no workspace_hashed_value'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Check `BaseWorkspaceSerializer` is valid.
            get_object_or_404(Workspace, hashed_value=workspace_hashed_value)

        user_status = self.get_queryset(Q(workspace__hashed_value__exact=workspace_hashed_value) &
                                        Q(until__gt=datetime.utcnow()))

        s = []
        for individual_status in user_status:
            s.append(self.get_serializer(individual_status, context=request))

        return Response(data=[stat.data for stat in s], status=status.HTTP_200_OK)
