from django.urls import path

from workspace.views import WorkspaceView

urlpatterns = [
    path('', WorkspaceView.as_view(), name='workspace')
]
