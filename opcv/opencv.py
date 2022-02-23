import cv2
from cv2 import dilate
from cv2 import imread
import numpy as np
import random
img=cv2.imread("test3.jpg")#img資料型態為陣列 py沒有 是numpy的資料型態
#陣列為很快的列表
#img = cv2.resize(img,(300,300))//調整大小為300*300
#img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)//寬高/2
#cv2.imshow('img',img)
#print(img.shape)#圖像大小
#cv2.waitKey(0)

'''vid=cv2.VideoCapture("html_test_video.mp4")
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
'''

#[b,g,r]
img2=np.empty((500,500,3),np.uint8)#0~255 2^8 -> uint"8" //創建多維陣列
for row in range(img2.shape[0]):
    for col in range(img2.shape[1]):
        if row<300:
            img2[row][col]=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        else:
            img2[row][col]=[0,255,0]
        

#cv2.imshow("img",img2)
#cv2.waitKey(0)

kernel=np.ones((2,2),np.uint8)#創建陣列 ones:數值都為1, (10,10):大小為10*10, np.unit8:範圍為0~255
'''test1=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#彩轉灰(三維陣列,cv2.COLOR_BGR2GRAY)
test2=cv2.GaussianBlur(img,(15,15),10)#高斯模糊(三維陣列,kernel核(二維陣列)!!必須為奇數!!,標準差)
test3=cv2.Canny(img,200,250)#邊緣圖片(三維陣列,最低門檻,最高門檻)
test4=cv2.dilate(test3,kernel,iterations=1)#加粗(三維陣列,kernel核(二維陣列),執行次數)
test5=cv2.erode(test4,kernel,iterations=1)#變細(三維陣列,kernel核(二維陣列),執行次數)
cv2.imshow("t1",test1)
cv2.imshow("t2",test2)
cv2.imshow("t3",test3)
cv2.imshow("t4",test4)
cv2.imshow("t5",test5)
cv2.waitKey(0)'''

'''
#畫圖
img3=np.zeros((600,600,3),np.uint8)
cv2.line(img3,(0,0),(400,400),(255,255,0),5)#畫直線(三維陣列,線的一端座標(x,y),線的另一端座標(x,y),顏色(b,g,r),粗度int)
#cv2.line(img3,(0,0),(img3.shape[0],img3.shape[1]),(255,255,0),10)
cv2.rectangle(img3,(0,0),(img3.shape[0],img3.shape[1]),(255,255,0),5)#畫方形(三維陣列,左上角座標(x,y),右下角座標(x,y),顏色(b,g,r),粗度int)
#cv2.rectangle(img3,(0,0),(img3.shape[0],img3.shape[1]),(255,255,0),cv2.FILLED)#cv2.FILLED為填滿
cv2.circle(img3,(img3.shape[0]//2,img3.shape[1]//2),img3.shape[0]//4,(255,255,0),5)#畫圓形(三維陣列,中心點座標(x,y),半徑int,顏色(b,g,r),粗度int)
cv2.putText(img3,"penis",(100,500),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),1)#寫字(三維陣列,文字內容,左下角座標(x,y),字形(cv2.FONT_可選),大小int,顏色(b,g,r),粗度int)!!不支援中文!!

cv2.imshow("img3",img3)
cv2.waitKey(0)

#import rex09pkg
#rex09pkg.drawpenis()
#cv2.waitKey(0)
'''

'''
#顏色偵測
img4=cv2.imread("test3.jpg")
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
'''

##輪廓檢測
#
#img5=imread("test3.jpg")
#img5Contour=img5.copy()#複製
#img5=cv2.cvtColor(img5,cv2.COLOR_BGR2GRAY)#輪廓檢測不需顏色
#canny=cv2.Canny(img5,150,200)
#contours,hierarchy=cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#偵測輪廓(三維陣列,使用模式(外輪廓或內輪廓或內外都要)(這邊為偵測外輪廓),近似方法(壓縮水平或垂直輪廓點)(這邊不壓縮))
##回傳所有輪廓(4維陣列),階乘(層?)
##輪廓為3維陣列
#for cnt in contours:
#    #print(cnt)#印出每個輪廓
#    cv2.drawContours(img5Contour,cnt,-1,(255,255,0),2)#畫出輪廓(要畫在甚麼圖形上面(三維陣列),要畫的輪廓點,要畫的輪廓是第幾個(?(-1為每個都畫),顏色,粗度)
#    area=cv2.contourArea(cnt)#取得輪廓面積(輪廓)
#    shapeName=("0","1","2","3","4","5","0","0","0","0","0")
#    if area>500:#過濾雜訊/噪點(當面積大於500再進行判斷)
#        #print(cv2.arcLength(cnt,True))#取得輪廓邊長(輪廓,輪廓是否為閉合)
#        peri=cv2.arcLength(cnt,True)
#        vertices=cv2.approxPolyDP(cnt,peri*0.02,True)#用多邊形近似輪廓(要近似的輪廓,近似值(越大多邊形的邊越多,反之越少)(此值可自行調整),輪廓是否為閉合)回傳多邊形頂點
#        corners=len(vertices)
#        x,y,w,h=cv2.boundingRect(vertices)#把每個圖形用方型框起來(三維陣列)回傳左上角xy座標跟方形的寬高
#        cv2.rectangle(img5Contour,(x,y),(x+w,y+h),(0,255,255),4)#畫出方型
#        for num in range(3,10):
#            if corners>10:
#                corners=10
#            cv2.putText(img5Contour,shapeName[corners],(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),4)
#
#cv2.imshow("img5",img5)
#cv2.imshow("img5",canny)
#cv2.imshow("img5Contour",img5Contour)
#cv2.waitKey(0)

#人臉辨識
#face_detect.xml為訓練好的人臉辨識模型
img6=cv2.imread("lenna.png")
gray=cv2.cvtColor(img6,cv2.COLOR_BGR2GRAY)
faceCas=cv2.CascadeClassifier("face_detect.xml")#載入人臉辨識模型
faceRec=faceCas.detectMultiScale(gray,1.1,3)#辨識人臉(圖片,每次圖片縮小的倍數,相鄰的框框最少要有幾個(該目標要被框到幾次才算偵測到))(回傳"所有"偵測到的臉(矩形框框xywh))
print(len(faceRec))
for (x,y,w,h) in faceRec:
    cv2.rectangle(img6,(x,y),(x+w,y+h),(255,255,0),2)

cv2.imshow("lenna",img6)
cv2.waitKey(0)


