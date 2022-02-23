import cv2
import numpy as np

vid=cv2.VideoCapture("html_test_video.mp4")
#vid=cv2.VideoCapture(0)#視訊鏡頭預設為0
faceCas=cv2.CascadeClassifier("face_detect.xml")#載入人臉辨識模型
while True:
    ret ,frame=vid.read()
    frame = cv2.resize(frame,(0,0),fx=0.5,fy=0.5)#//寬高/2
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faceRec=faceCas.detectMultiScale(gray,1.1,1)
    if ret:
        for (x,y,w,h) in faceRec:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
            cv2.imshow("video",frame)
    else:
        break
    if cv2.waitKey(35)==ord('q'):
        break