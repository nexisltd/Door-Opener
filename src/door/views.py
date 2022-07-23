import json
from time import sleep

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import render

from . import settings


def index(request):
    return render(request, 'index.html', context={'link': settings.WEBCAM_IP})


class DoorConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = 'test'

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data = json.loads(text_data)
        message = text_data['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': "door_open",
            }
        )

        timeoutLimit = 10
        for time in range(timeoutLimit):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    'type': "timer",
                    'message': timeoutLimit - time
                }
            )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': "door_close",
            }
        )

    def door_open(self, event):
        self.send(text_data=json.dumps({
            'type': 'door_handler',
            'message': "Open"
        }))

    def door_close(self, event):
        self.send(text_data=json.dumps({
            'type': 'door_handler',
            'message': "Close"
        }))

    def timer(self, event):
        sleep(1)
        self.send(text_data=json.dumps({
            'type': 'timer',
            'message': event['message']
        }))

    # def door_handler(self, event):
    #     timeoutLimit = 10
    #     if event['type'] == 'door_handler' and event['message'] == 'Open':
    #         self.send(text_data=json.dumps(
    #             {'type': event['type'], 'message': 'Open'}))
    #         for seconds in range(timeoutLimit):
    #             self.send(text_data=json.dumps(
    #                 {'type': 'timer', 'message': (timeoutLimit-seconds)}))
    #             sleep(1)
    #         self.send(text_data=json.dumps(
    #             {'type': event['type'], 'message': 'Close'}))
