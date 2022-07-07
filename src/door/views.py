import time
from tkinter import Frame
from zk import ZK
from django.views import View
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
import requests

import cv2
from . import settings

import asyncio
import json
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from base64 import b64encode, b64decode


class LiveWebCam(object):
    def __init__(self):
        self.url = cv2.VideoCapture(
            f'rtsp://{settings.WEBCAM_USER}:{settings.WEBCAM_PASSWORD}@{settings.WEBCAM_IP}:{settings.WEBCAM_PORT}')

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        success, imgNp = self.url.read()
        resize = cv2.resize(imgNp, (640, 480), interpolation=cv2.INTER_LINEAR)
        ret, jpeg = cv2.imencode('.jpg', resize)
        return jpeg.tobytes()


def gen(camera):
    # while True:
    frame = camera
    # frame = b64encode(frame)
    return frame
    # return (b'--frame\r\n'
    #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def index(request):
    return render(request, 'index.html')


def door_open(request):
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
        print("Process terminate : {}".format(e))
    finally:
        if conn:
            conn.disconnect()
    return render(request, 'index.html')


class DoorConsumer(WebsocketConsumer):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.stop = True

    def connect(self):
        self.accept()

        # while self.stop:
        #     self.send(bytes_data=gen(live.get_frame()))
        # while True:
        #     self.send(bytes_data=gen(live.get_frame()))
        live = LiveWebCam()
        while True:
            while self.connect():
                self.send(bytes_data=gen(live.get_frame()))

    def disconnect(self, code):
        raise StopConsumer()

    # def send_message(self, text_data=None, bytes_data=None, close=False):
    #     live = LiveWebCam()
    #     print("hidhk")
    #     while True:
    #         self.send(text_data=gen(live.get_frame()))
