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
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
        # success, image = frame.read()
        # count = 1
        # while success:
        #     cv2.imwrite("video_data/image_%d.jpg" % count, image)    
        #     success, image = frame.read()
        #     print('Saved image ', count)
        #     count += 1


def livecam_feed(request):
    # print(type(gen(LiveWebCam())))
    return StreamingHttpResponse(gen(LiveWebCam()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


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
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'type':'connection_established',
            'message':'You are connected!'
        }))
        self.send(gen(LiveWebCam()),content_type='multipart/x-mixed-replace; boundary=frame')
        
    # def livecam_feed(request):
    #     return StreamingHttpResponse(gen(LiveWebCam()),
    #                                 content_type='multipart/x-mixed-replace; boundary=frame')