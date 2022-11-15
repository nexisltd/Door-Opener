from django.conf import settings
from ml import models
from rest_framework import generics
from door.views import Door
import cv2
import face_recognition
import numpy as np
from time import sleep


class ML(generics.ListAPIView):
    video_capture = cv2.VideoCapture(settings.WEBCAM_IP)
    # Load a sample picture and learn how to recognize it.
    known_face_encodings = []
    img = models.DoorModel.objects.all()
    for i in img:
        image = face_recognition.load_image_file(i.pic)
        face_encoding = face_recognition.face_encodings(image)[0]

        # Create arrays of known face encodings and their names
        if face_encoding not in known_face_encodings:
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
                first_match_index = matches.index(True)
                Door()
                sleep(10)
