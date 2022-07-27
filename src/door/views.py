import asyncio

from zk import ZK
from django.shortcuts import render
from rest_framework import response, status, exceptions
from rest_framework.views import APIView
from . import settings
# from time import sleep
from asyncio import sleep
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync


def index(request):
    return render(request, 'index.html', context={'link': settings.WEBCAM_IP})


class Door(APIView):
    def get(self, request):
        conn = None
        zk = ZK(f'{settings.ZK_IP}', port=4370, timeout=5, password=f'{settings.ZK_PASSWORD}', force_udp=False,
                ommit_ping=False)
        try:
            conn = zk.connect()
            conn.disable_device()
            conn.test_voice()
            conn.unlock(time=1)
            conn.enable_device()
        except Exception as e:
            raise exceptions.PermissionDenied(detail=f"Process terminate : {e}")
        finally:
            if conn:
                conn.disconnect()

        return response.Response({'detail': 'Door has been open'},
                                 status=status.HTTP_200_OK)


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

    async def receive(self, text_data):
        text_data = json.loads(text_data)
        message = text_data['message']
        if text_data == {'message': 'Open'}:
            time = 10
            while time:
                await self.channel_layer.group_send(
                    self.room_group_name, {
                        'type': 'door_message',
                        'time': time,
                        'message': message,
                    }
                )
                time -= 1

    async def door_message(self, event):
        message = event['message']
        time = event['time']
        await sleep(1)
        await self.send(text_data=json.dumps({
            'type': 'door',
            'message': message,
            'time': time
        }))
