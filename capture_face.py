#! /usr/bin/python2
import cv2
import sys
from detectface import FaceRecognizer
from detectface import ConsistentFace

try:
    import controlTurret
except ImportError:
    class controlTurret:

        @staticmethod
        def setup_usb():
            pass

        @staticmethod
        def move_turret(x):
            pass
    print "Install PYUSB to control the turret"


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

#video_file = cv2.VideoWriter("demo2.avi", cv2.cv.CV_FOURCC('X','V','I','D'), 24, (960, 540), True)

faceRecognizer = FaceRecognizer(classifer_type)

try:
    controlTurret.setup_usb()
except ValueError:
    print "Could not control turret"

consistentFaces = []

confidenceThreshold = 100

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
            if y < 0 or y + h >= gray.shape[0]:
                continue
            face_image = gray[y:y + h, x:x + w]
            if face_image.size < 32:
                continue
            name, confidence = faceRecognizer.detect_face(face_image)
            new = True
            myid = id
            visible = False
            for consistentFace in consistentFaces:
                if consistentFace.match(x, y, w, h):
                    consistentFace.update(
                        x, y, w, h, name, confidence, face_image)
                    name = consistentFace.name
                    confidence = consistentFace.confidence
                    new = False
                    myid = consistentFace.id
                    visible = not consistentFace.invisible
                    break
            # print name, confidence
            if new:
                consistentFaces.append(
                    ConsistentFace(x, y, w, h, name, confidence, id, face_image))
                id += 1
            if not visible:
                pass
            elif confidence < confidenceThreshold and str(name) == 'modi':
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(
                    frame, str(myid), (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                cv2.putText(frame, 'face ' + str(name) + ' (' + str(int(confidence)) + ')',
                            (x + 20, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
            elif confidence < confidenceThreshold:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    frame, str(myid), (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                cv2.putText(frame, 'face ' + str(name) + ' (' + str(int(confidence)) + ')',
                            (x + 20, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(
                    frame, str(myid), (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                cv2.putText(frame, 'face ' + str(name) + ' (' + str(int(confidence)) + ')',
                            (x + 20, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
        #for face in consistentFaces:
        #    print face.id
        for f in reversed(consistentFaces):
            if not f.stillalive():
                consistentFaces.remove(f)

    # Display the resulting frame
    #video_file.write(frame)
    cv2.imshow('Video', frame)


    #key = cv2.waitKey(100) & 0xFF
    #if key == ord('q'):
    #    break
    #controlTurret.move_turret(chr(key))


# When everything is done, release the capture
#video_file.release()
video_capture.release()
cv2.destroyAllWindows()
