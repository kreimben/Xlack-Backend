from datetime import datetime

from asgiref.sync import async_to_sync
from django.db.models import Q

from status.models import UserStatus
from websocket.AuthWebsocketConsumer import AuthWebsocketConsumer
from workspace.models import Workspace


class StatusConsumer(AuthWebsocketConsumer):
    workspace: Workspace | None = None

    async def before_accept(self):
        kwargs = self.scope["url_route"]["kwargs"]
        self.room_group_name = kwargs.get('workspace_hashed_value')

    async def after_accept(self):
        # Check workspace `hashed_value` is valid.
        try:
            self.workspace = await Workspace.objects.prefetch_related('members').aget(
                hashed_value=self.room_group_name
            )
        except Workspace.DoesNotExist:
            await self.send_json({
                'success': False,
                'msg': 'No such workspace. Not found.'
            }, close=True)

    async def after_auth(self):
        if self.user not in self.workspace.members.all():
            await self.send_json({
                'success': False,
                'msg': f'{self.user} is not in workspace.'
            }, close=True)
        else:
            await super().after_auth()

    message_field = ['status_message', 'status_icon', 'until']

    async def from_client(self, content, **kwargs):
        data = {'type': 'status.broadcast'}
        not_filled = []
        for field in self.message_field:
            if content.get(field, None) is None:
                not_filled.append(field)

        if len(not_filled):
            await self.send_json(content={'msg': f'Not filled this fields: {not_filled}'})
        else:
            try:
                status = UserStatus.objects.get(user=self.user)
                status.message = content.get('status_message')
                status.icon = content.get('status_icon')
                status.until = content.get('until')
                status.save()
                del status
            except UserStatus.DoesNotExist:
                workspace = Workspace.objects.get(hashed_value__exact=self.room_group_name)
                UserStatus.objects.create(
                    message=content.get('status_message'),
                    icon=content.get('status_icon'),
                    until=content.get('until'),
                    workspace=workspace,
                    user=self.user
                )
                del workspace

            # Refine data.
            print(f'{datetime.utcnow()=}')
            user_status = UserStatus.objects.prefetch_related('workspace') \
                .filter(Q(workspace__hashed_value__exact=self.room_group_name) &
                        Q(until__gt=datetime.utcnow()))

            result = []
            for status in user_status:
                status: UserStatus
                d = {}
                d['message'] = status.message
                d['icon'] = status.icon
                d['until'] = status.until.strftime('%Y-%m-%d %H:%M%z')
                d['user_id'] = status.user_id
                d['workspace_id'] = status.workspace_id
                result.append(d)
            data['users_status'] = result

            # Broadcast refined data.
            await self.channel_layer.group_send(
                self.room_group_name,
                data
            )

    async def status_broadcast(self, event):
        """
        This function speaks message to every body in this group.
        """
        await self.send_json(event['users_status'])
