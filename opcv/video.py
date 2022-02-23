import cv2
from cv2 import dilate
from cv2 import imread
import numpy as np
import random
vid=cv2.VideoCapture(0)
#vid=cv2.VideoCapture(0)#視訊鏡頭預設為0
while True:
    ret ,frame=vid.read()
    frame = cv2.resize(frame,(0,0),fx=2,fy=2)#//寬高/2
    if ret:
        cv2.imshow("video",frame)
    else:
        break
    if cv2.waitKey(40)==ord('q'):
        break
