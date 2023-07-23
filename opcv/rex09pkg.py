#need:
#pip install opencv-python

import cv2
import numpy
def drawpenis():   
    penis=numpy.zeros((600,600,3),numpy.uint8)
    cv2.circle(penis,(300,200),70,(206,235,248),5)
    cv2.rectangle(penis,(185,200),(375,275),(0,0,0),cv2.FILLED)
    cv2.line(penis,(230,200),(370,200),(206,235,248),5)
    cv2.line(penis,(300,130),(300,160),(206,235,248),5)
    cv2.line(penis,(250,200),(250,400),(206,235,248),5)
    cv2.line(penis,(350,200),(350,400),(206,235,248),5)
    cv2.circle(penis,(250,450),50,(206,235,248),5)
    cv2.circle(penis,(350,450),50,(206,235,248),5)
    cv2.rectangle(penis,(254,395),(346,460),(0,0,0),cv2.FILLED)
    cv2.imshow("penis",penis)
    cv2.waitKey(0)
    return 0