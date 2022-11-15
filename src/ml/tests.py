# known_face_names = []
known_face_encodings = []
img = ["e", "t", "f", "t", "k"]
for i in img:
    face_encoding = i

    # Create arrays of known face encodings and their names
    if face_encoding not in known_face_encodings:
        known_face_encodings.append(face_encoding)
print(known_face_encodings)
