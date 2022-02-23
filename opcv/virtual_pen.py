from unittest import result
import cv2
from cv2 import dilate
from cv2 import imread
from cv2 import VideoCapture
import numpy as np
import random
vid=cv2.VideoCapture(0)
lower=np.array([21,48,91])
upper=np.array([34,228,255])


while True:
    ret ,frame=vid.read()
    vhsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(vhsv,lower,upper)
    result=cv2.bitwise_and(frame,frame,mask=mask)
    result=cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    canny=cv2.Canny(result,150,200)
    contours,hierarchy=cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    maxArea=0
    for cnt in contours:
        #print(cnt)#印出每個輪廓
        cv2.drawContours(frame,cnt,-1,(255,255,0),2)#畫出輪廓(要畫在甚麼圖形上面(三維陣列),要畫的輪廓,要畫的輪廓是第幾個(?(-1為每個都畫),顏色,粗度)
        area=cv2.contourArea(cnt)#取得輪廓面積(輪廓)
        #if area>maxArea:
        #    maxArea=area
        if area>100:#過濾雜訊/噪點(當面積大於500再進行判斷)
            #print(cv2.arcLength(cnt,True))#取得輪廓邊長(輪廓,輪廓是否為閉合)
            peri=cv2.arcLength(cnt,True)
            vertices=cv2.approxPolyDP(cnt,peri*0.02,True)#用多邊形近似輪廓(要近似的輪廓,近似值(越大多邊形的邊越多,反之越少)(此值可自行調整),輪廓是否為閉合)回傳多邊形頂點
            corners=len(vertices)
            x,y,w,h=cv2.boundingRect(vertices)#把每個圖形用方型框起來(三維陣列)回傳左上角xy座標跟方形的寬高
            cv2.circle(frame,(x+(w//2),y+(h//2)),50,(255,255,0),cv2.FILLED)#畫圓形(三維陣列,中心點座標(x,y),半徑int,顏色(b,g,r),粗度int)
    #print(maxArea)
    cv2.imshow("video",frame)
    cv2.imshow("canny",canny)
    if cv2.waitKey(40)==ord('q'):
        break