import json
from asyncio import sleep

# from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import render

from . import settings


def index(request):
    return render(request, 'index.html', context={'link': settings.WEBCAM_IP})


class DoorConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = 'test'

    async def connect(self):
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'new_client',
            }
        )

    async def receive(self, text_data):
        text_data = json.loads(text_data)
        message = text_data['message']
        msg_type = text_data['type']

        if msg_type == 'door_handler' and message == 'Open':
            timeout_limit = 30
            for seconds in range(timeout_limit):
                await self.channel_layer.group_send(
                    self.room_group_name, {'type': 'timer', 'message': (timeout_limit - seconds)}
                )
            await self.channel_layer.group_send(
                self.room_group_name, {'type': 'door_close'}
            )

    async def new_client(self, event):
        await self.send(text_data=json.dumps({
            'type': 'client',
            'message': f"Connected new client in {self.room_group_name}"
        }))

    async def timer(self, event):
        await sleep(1)
        await self.send(text_data=json.dumps({
            'type': 'timer',
            'message': event['message']
        }))

    async def door_close(self, event):
        await self.send(text_data=json.dumps({
            'type': 'door_handler',
            'message': "Close"
        }))
