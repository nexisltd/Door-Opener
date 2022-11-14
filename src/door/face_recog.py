import cv2
import face_recognition
import numpy as np

video_capture = cv2.VideoCapture('https://doorcam.local.nexisltd.com')
count = 0
# Load a sample picture and learn how to recognize it.
emon_image = face_recognition.load_image_file("emon.jpg")
emon_face_encoding = face_recognition.face_encodings(emon_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    emon_face_encoding,
]
known_face_names = [
    "Istiak Hassan Emon",
]

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            print(name, count)
            count = count +1