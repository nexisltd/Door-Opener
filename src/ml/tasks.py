import platform  # For getting the operating system name
import subprocess  # For executing a shell command
from time import sleep

import cv2
import face_recognition
from celery import shared_task
from django.conf import settings
from zk import ZK

from door.views import Door
from ml import models


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = "-n" if platform.system().lower() == "windows" else "-c"

    # Building the command. Ex: "ping -c 1 google.com"
    command = ["ping", param, "1", host]

    return subprocess.call(command) == 0


@shared_task(bind=True)
def ML(self, *args, **kwargs):
    while True:
        if ping(settings.WEBCAM_IP):
            video_capture = cv2.VideoCapture(0)
            break
        sleep(60)

    # Load a sample picture and learn how to recognize it.
    known_face_encodings = []
    img = models.DoorModel.objects.all()
    for i in img:
        image = face_recognition.load_image_file(i.pic)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(
            face_locations, face_encodings
        ):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding
            )
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                print("matched")
                Door()
                sleep(10)
                matches = []
