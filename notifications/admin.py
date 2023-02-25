from django.contrib import admin, messages

from notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "sender", "receiver", 'chat', "channel", "had_read"]
    search_fields = ["sender", "receiver", "channel"]
    list_filter = ['sender', 'receiver', 'channel', 'had_read']
    actions = ['make_read', 'make_unread']
    list_select_related = ['sender', 'receiver', 'channel']

    @admin.action(description='선택한 알림들을 읽음 처리 합니다.')
    def make_read(self, request, queryset):
        queryset.update(had_read=True)
        self.message_user(request,
                          f'{len(queryset)}개의 알림이 읽음 처리 됐습니다.',
                          messages.SUCCESS)

    @admin.action(description='선택한 알림들을 안읽음 처리 합니다.')
    def make_unread(self, request, queryset):
        queryset.update(had_read=False)
        self.message_user(request,
                          f'{len(queryset)}개의 알림이 안읽음 처리 됐습니다.',
                          messages.SUCCESS)
