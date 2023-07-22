#顏色偵測
import cv2
from cv2 import dilate
from cv2 import imread
import numpy as np
import random
img4=cv2.imread("test3.jpg")#錯誤可以改成絕對路徑試試
hsv=cv2.cvtColor(img4,cv2.COLOR_BGR2HSV)#bgr轉hsv
#hsv:色調(各種顏色),飽和度(白~彩),亮度(黑~亮)

cv2.namedWindow("trackbar")#建立視窗(視窗名稱)
cv2.resizeWindow("trackbar",640,320)#調整視窗大小(視窗名稱,寬,高)

def empty(v):
    pass#跳過不管
cv2.createTrackbar("Hue Min","trackbar",0,179,empty)#建立控制條(名稱,所在視窗名稱,初始值,最大值(opcv的hue最大可到179),當值被改變時所要呼叫的函式(會傳一個值進去))
cv2.createTrackbar("Hue Max","trackbar",179,179,empty)
cv2.createTrackbar("Sat Min","trackbar",0,255,empty)
cv2.createTrackbar("Sat Max","trackbar",255,255,empty)
cv2.createTrackbar("Val Min","trackbar",0,255,empty)
cv2.createTrackbar("Val Max","trackbar",255,255,empty)

while True:
    h_min=cv2.getTrackbarPos("Hue Min","trackbar")#取控制條的值(控制條名稱,視窗名稱)
    h_max=cv2.getTrackbarPos("Hue Max","trackbar")
    s_min=cv2.getTrackbarPos("Sat Min","trackbar")
    s_max=cv2.getTrackbarPos("Sat Max","trackbar")
    v_min=cv2.getTrackbarPos("Val Min","trackbar")
    v_max=cv2.getTrackbarPos("Val Max","trackbar")
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    mask=cv2.inRange(hsv,lower,upper)#過濾顏色-顯示遮罩(三維陣列,最小值(陣列(存hsv三個值)),最大值(陣列(存hsv三個值)))
    result=cv2.bitwise_and(img4,img4,mask=mask)#過濾顏色-顯示結果(三維陣列(原圖),三維陣列(原圖),mask=三維陣列(遮罩))
    
    cv2.imshow("hsv",hsv)
    cv2.imshow("mask",mask)
    cv2.imshow("result",result)
    cv2.waitKey(1)
cv2.imshow("hsv",hsv)
cv2.imshow("mask",mask)
cv2.waitKey(0)