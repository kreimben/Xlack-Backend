from datetime import datetime

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth.models import User
from django.db.models import Q

from AuthHelper import AuthHelper, AccessTokenNotIncludedInHeader
from custom_user.models import CustomUser
from status.models import UserStatus
from workspace.models import Workspace


class StatusConsumer(JsonWebsocketConsumer):
    def connect(self):
        kwargs = self.scope["url_route"]["kwargs"]
        self.room_group_name = kwargs.get('workspace_hashed_value')

        # Check auth first.
        try:
            user = AuthHelper.find_user(self.scope)
        except AccessTokenNotIncludedInHeader:
            print(f'access token was not in header.')
            return
        except CustomUser.DoesNotExist:
            print(f'No such user.')
            return

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # Check workspace `hashed_value` is valid.
        try:
            w: Workspace = Workspace.objects.prefetch_related('members').get(
                hashed_value=kwargs.get('workspace_hashed_value'))
            all_users_in_workspace: [User] = w.members.all()  # Have to find better way to find a user.
        except Workspace.DoesNotExist as e:
            print(f'{e}')
            return

        if user not in all_users_in_workspace:
            print(f'{user} is not in workspace')
            return

        self.accept()
        self.send_json(content={'user_id': user.id})

    message_field = ['status_message', 'status_icon', 'until']

    def receive_json(self, content, **kwargs):
        """
        Find user model using access token.
        And check what fields are unfilled.
        If no problem, Send message to everyone.
        """
        try:
            user = AuthHelper.find_user(self.scope)
        except AccessTokenNotIncludedInHeader:
            print(f'access token was not in header.')
            self.send_json(content={'msg': 'access token was not in header.'}, close=True)
            return
        except CustomUser.DoesNotExist:
            print(f'No such user.')
            self.send_json(content={'msg': 'No such user.'}, close=True)
            return

        data = {'type': 'status.broadcast'}
        not_filled = []
        for field in self.message_field:
            if content.get(field, None) is None:
                not_filled.append(field)

        if len(not_filled):
            self.send_json(content={'msg': f'Not filled this fields: {not_filled}'})
        else:
            try:
                status = UserStatus.objects.get(user=user)
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
                    user=user
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
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                data
            )

    def status_broadcast(self, event):
        """
        This function speaks message to every body in this group.
        """
        print(f'{event=}')
        self.send_json(event['users_status'])

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        raise StopConsumer()
