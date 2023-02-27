from django.urls import path

from workspace.views import WorkspaceView, WorkspaceBookmarkedChatView

urlpatterns = [
    path('', WorkspaceView.as_view(), name='workspace'),
    path('bookmarked_chat/<str:workspace_hashed_value>', WorkspaceBookmarkedChatView.as_view(), name='workspace_bookmarked_chats'),
]
