from zk import ZK
from django.views import View
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from rest_framework import response, status, exceptions
from rest_framework.views import APIView
import cv2
from . import settings

import json
from channels.generic.websocket import AsyncWebsocketConsumer


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
    async def connect(self):
        await self.accept()
        print('connection open')

    async def disconnect(self, close_code):
        print('disconnect')

    async def receive(self, text_data):
        print('receive')
