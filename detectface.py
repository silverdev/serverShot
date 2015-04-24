import cv2
from cv2 import cv
import csv
import numpy as np
import time

class Face(object):

    def __init__(self, image, label=None):
        self.image = image
        self.label = label


def read_faces(csv_url):
    with open("faces.csv", "rb") as f:
        doc = csv.reader(f, delimiter=';')
        face_urls = list(doc)
    faces = list()
    names = list()
    samples = list()
    print face_urls[0]
    for face_url, name, sample in face_urls:
        face = cv2.imread(face_url)
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        faces.append(face)
        names.append(name)
        samples.append(sample)
        timeShow(face)
        print name
    return faces, names, samples


class FaceRecognizer(object):
    def __init__(self, mode=0, csv_url="faces.csv"):
        self.faces, self.names, self.samples = read_faces(csv_url)
        self.face_y, self.face_x = self.faces[0].shape
        self.face_size = self.faces[0].shape
        print self.faces[0].shape
        if mode == 0:
            self.model = cv2.createEigenFaceRecognizer(num_components=80)
        if mode == 1:
            self.model =cv2.createLBPHFaceRecognizer(neighbors=32,grid_x=16, grid_y=16)
        if mode == 2:
            self.model =cv2.createFisherFaceRecognizer(num_components=80)
        self.model.train(self.faces, np.array(range(len(self.names))))

    def detect_face(self, image):
        if image.shape != self.face_size:
            image = cv2.resize(image, (self.face_x, self.face_y), None, 0, 0,
                               cv2.INTER_NEAREST)
        timeShow(image)
        index, confidence = self.model.predict(image)
        label = self.names[index]
        print index, label, confidence, self.samples[index]
        return label, True if confidence < 100 else False


def timeShow(img):
    cv2.imshow('pic', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()

    for x in range(1000):
        pass
    #time.sleep(4)
