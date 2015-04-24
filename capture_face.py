#! /usr/bin/python2
import cv2
import sys
from detectface import FaceRecognizer
from detectface import ConsistentFace


print sys.argv[0]


def list_get(l, idx):
    try:
        return l[idx]
    except IndexError:
        return None

cascPath = sys.argv[1]

classifer_type = int(list_get(sys.argv, 2) or "1")
url = list_get(sys.argv, 3) or 0


faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(url)

faceRecognizer = FaceRecognizer(classifer_type)



consistentFaces = []

confidenceThreshold = 1000

id = 0
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
            name, confidence = faceRecognizer.detect_face(face_image)
            new = True
            myid = id
            for consistentFace in consistentFaces:
                if consistentFace.match(x, y, w, h):
                    consistentFace.update(x, y, w, h, name, confidence, face_image)
                    name = consistentFace.name
                    confidence = consistentFace.confidence
                    new = False
                    myid = consistentFace.id
                    break
            #print name, confidence
            if new:
                consistentFaces.append(ConsistentFace(x, y, w, h, name, confidence, id, face_image))
                id += 1
            if confidence < confidenceThreshold:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, str(myid), (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0))
                cv2.putText(frame, 'face '+str(name), (x+20, y), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0))
                cv2.putText(frame, '('+str(int(confidence))+')', (x+95, y), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0))
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,  0, 255), 2)
                cv2.putText(frame, str(myid), (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0))
                cv2.putText(frame, 'face '+str(name), (x+20, y), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0))
                cv2.putText(frame, '('+str(int(confidence))+')', (x+95, y), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0))
        for face in consistentFaces:
            print face.id
        for f in reversed(consistentFaces):
            if not f.stillalive():
                consistentFaces.remove(f)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
