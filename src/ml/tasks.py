
from time import sleep

import cv2
import face_recognition
from celery import shared_task
from django.conf import settings
from zk import ZK
from ml import models




@shared_task(bind=True)
def ML(self, *args, **kwargs):
    """
    It takes a picture from the camera, compares it to the pictures in the database, if it finds a
    match, it opens the door
    """
    video_capture = cv2.VideoCapture(settings.ML_CAM_IP)

    # Load a sample picture and learn how to recognize it.
    known_face_encodings = []
    img = models.DoorModel.objects.all()
    for i in img:
        image = face_recognition.load_image_file(i.pic)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
    matches=[]

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
        # If a match was found in known_face_encodings, open the door and clean previous matches.
        if matches:
            print("matched")
            Door()
            sleep(10)
        matches=[]
    

def Door():
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
        print(e)
    finally:
        if conn:
            conn.disconnect()