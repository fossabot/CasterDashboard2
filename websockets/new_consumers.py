import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class MatchDataConsumer2(JsonWebsocketConsumer):

    # Connect new client
    def connect(self):
        # Get room group
        self.group_name = 'match_data_' + self.scope['url_route']['kwargs']['user']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    # Disconnect client
    def disconnect(self, code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive from client and send to group
    def receive_json(self, content, **kwargs):
        from django.contrib.auth.models import User
        from overlays.models.models import MatchOverlayData
        from dashboard.models.serializers import MatchSerializer

        # Send data on request
        if content.get('command') == 'get_match_data':
            user_id = User.objects.get(username=self.scope['url_route']['kwargs']['user']).id
            match = MatchOverlayData.objects.get(user=user_id).current_match

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'send_to_client',
                    'data': MatchSerializer(match).data
                }
            )

    # Send from group to client
    def send_to_client(self, event):
        self.send_json(event['data'])


class MatchMapConsumer2(JsonWebsocketConsumer):

    # Connect new client
    def connect(self):
        # Get room group
        self.group_name = 'match_map_' + self.scope['url_route']['kwargs']['user']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    # Disconnect client
    def disconnect(self, code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive from client and send to group
    def receive_json(self, content, **kwargs):
        from django.contrib.auth.models import User
        from overlays.models.models import MatchOverlayData
        from dashboard.models.models import MatchMap
        from dashboard.models.serializers import MatchMapSerializer

        # Send data on request
        if content.get('command') == 'get_match_map':
            user_id = User.objects.get(username=self.scope['url_route']['kwargs']['user']).id
            match = MatchOverlayData.objects.get(user=user_id).current_match
            try:
                match_map = MatchMap.objects.get(match=match, status=2)
            except MatchMap.DoesNotExist:
                return

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'send_to_client',
                    'data': MatchMapSerializer(match_map).data
                }
            )

    # Send from group to client
    def send_to_client(self, event):
        self.send_json(event['data'])


class OverlayStateConsumer2(JsonWebsocketConsumer):

    # Connect new client
    def connect(self):
        # Get room group
        self.group_name = 'overlay_state_' + self.scope['url_route']['kwargs']['user']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    # Disconnect client
    def disconnect(self, code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive from client and send to group
    def receive_json(self, content, **kwargs):
        from django.contrib.auth.models import User
        from overlays.models.models import OverlayState
        from overlays.models.serializers import OverlayStateSerializer

        # Send data on request
        if content.get('command') == 'get_overlay_state':
            user_id = User.objects.get(username=self.scope['url_route']['kwargs']['user']).id
            overlay_state = OverlayState.objects.get(user=user_id)

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'send_to_client',
                    'data': OverlayStateSerializer(overlay_state).data
                }
            )

    # Send from group to client
    def send_to_client(self, event):
        self.send_json(event['data'])
