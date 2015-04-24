#! /usr/bin/python2
import cv2
import sys
from detectface import FaceRecognizer


print sys.argv[0]

cascPath = sys.argv[1]
url = sys.argv[2]

faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(url)

faceRecognizer = FaceRecognizer()

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC3)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    if len(faces) > 0:


        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            ar = (w * 112) / 92 - h
            y -= ar / 2
            h += ar / 2
            if y < 0 or y+h >= gray.shape[0]:
                continue
            face_image = gray[y:y+h, x:x+w]
            if face_image.size < 32:
                continue
            name, auth = faceRecognizer.detect_face(face_image)
            if auth:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,  0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
