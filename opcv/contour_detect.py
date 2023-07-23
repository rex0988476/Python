#輪廓檢測
import cv2
from cv2 import dilate
from cv2 import imread
import numpy as np
import random

img5=imread("test3.jpg")
img5Contour=img5.copy() #複製
img5=cv2.cvtColor(img5,cv2.COLOR_BGR2GRAY)#輪廓檢測不需顏色
canny=cv2.Canny(img5,150,200)
contours,hierarchy=cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#偵測輪廓(三維陣列,使用模式(外輪廓或內輪廓或內外都要)(這邊為偵測外輪廓),近似方法(壓縮水平或垂直輪廓點)(這邊不壓縮))
#回傳所有輪廓(4維陣列),階乘(層?)
#輪廓為3維陣列
for cnt in contours:
    #print(cnt)#印出每個輪廓
    cv2.drawContours(img5Contour,cnt,-1,(255,255,0),2)#畫出輪廓(要畫在甚麼圖形上面(三維陣列),要畫的輪廓,要畫的輪廓是第幾個(?(-1為每個都畫),顏色,粗度)
    area=cv2.contourArea(cnt)#取得輪廓面積(輪廓)
    shapeName=("0","1","2","3","4","5","0","0","0","0","0")
    if area>500:#過濾雜訊/噪點(當面積大於500再進行判斷)
        #print(cv2.arcLength(cnt,True))#取得輪廓邊長(輪廓,輪廓是否為閉合)
        peri=cv2.arcLength(cnt,True)
        vertices=cv2.approxPolyDP(cnt,peri*0.02,True)#用多邊形近似輪廓(要近似的輪廓,近似值(越大多邊形的邊越多,反之越少)(此值可自行調整),輪廓是否為閉合)回傳多邊形頂點
        corners=len(vertices)
        x,y,w,h=cv2.boundingRect(vertices)#把每個圖形用方型框起來(三維陣列)回傳左上角xy座標跟方形的寬高
        cv2.rectangle(img5Contour,(x,y),(x+w,y+h),(0,255,255),4)#畫出方型
        for num in range(3,10):
            if corners>10:
                corners=10
            cv2.putText(img5Contour,shapeName[corners],(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),4)

cv2.imshow("img5",img5)
cv2.imshow("img5c",canny)
cv2.imshow("img5Contour",img5Contour)
cv2.waitKey(0)