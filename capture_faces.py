import numpy as np
import cv2
import datetime
import dlib
import face_landmarks
import ck_landmarks_extraction
import sys
from sklearn import svm

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
landmarks_predictor = face_landmarks.faceLandmarks("shape_predictor_68_face_landmarks.dat")

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]

print "Exracting training data from dataset"
features, labels = ck_landmarks_extraction.get_training_data(sys.argv[1], sys.argv[2])

print "Init Support Vector Machine"
clf = svm.SVC(gamma=0.001, C=200.)
clf.fit(features, labels)

cap = cv2.VideoCapture(0)

while(True):
    #t0 = datetime.datetime.now()
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        rect = dlib.rectangle(long(x), long(y), long(x+w), long(y+h))
        landmarks = landmarks_predictor.get_landmarks(frame, rect)
        pred = clf.predict([landmarks])
        print pred, emotions[pred[0]]
        #cv2.circle(frame, (tl_rect[0], tl_rect[1]), 3, (255,0,0))
        #for p in landmarks_predictor(gray, rect).parts():
            #cv2.circle(frame, (p.x, p.y), 3, (255,0,0))

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #print "time: ", (datetime.datetime.now() - t0)

cap.release()
cv2.destroyAllWindows()
