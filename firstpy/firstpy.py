#cls
###alt+shift+滑鼠左鍵=同時多行
name="WHITE"
age=87
is_male=True
print("我是"+name)
#''和""皆可表示字串
#[字串].lower() //將[字串]轉小寫後回傳(String)
#[字串].upper() //將[字串]轉大寫後回傳(String)
#[字串].isupper() //判斷[字串]是否全為大寫,回傳(boolen)
#[字串].islower() //判斷[字串]是否全為小寫,回傳(boolen)
#[字串].lower().islower() //.可連續使用,回傳最後函式的回傳型態
#[字串][[數字]] //回傳該數字index(從0開始)的(char)
#[字串].index("[char]") //回傳最早出現該字元的index(int)
#[字串].replace("[替換前字元]","[替換後字元]") //將[字串]中的[替換前字元]換成[替換後字元]後回傳(String)
L="WHITE"
print(L.lower())
print("小黑".lower())
U="black"
print(U.upper())

print(8+5)
print(8//5)# '//'為整數除法
#str([數字]) //將[數字]轉字串後回傳(string)
#abs([數字]) //將[數字]取絕對值後回傳(int)
#pow([數字1],[數字2]) //計算[數字1]的[數字2]次方後回傳(int)
#max([數字],[數字],[數字],...) //傳入任意數量的[數字]並回傳最大值
#min([數字],[數字],[數字],...) //傳入任意數量的[數字]並回傳最小值
#round([浮點數]) //將[浮點數]四捨五入後回傳(int)
#from math import * //引入math函式庫
#floor([浮點數]) //將[浮點數]無條件捨去後回傳(int)
#ceil([浮點數]) //將[浮點數]無條件進位後回傳(int)
#sqrt([數字]) //將[數字]開根號後回傳(int)||(float)
from math import *
print(sqrt(3.5))

#[變數] = input("[提示字串]") //將鍵盤輸入值存到[變數]裡面(string)
#int([字串]) //將[字串]轉數字後回傳(int)
#float([字串]) //將[字串]轉浮點數後回傳(float)

#[變數]=[[值],[值],[值],[值],...] //列表list(類似陣列)
l=[1,2,3,4,5]
print(l)
#同一列表可存放不同資料型態
s=[1,2.0,"3"]

#[列表][[數字]] //回傳該數字index(從0開始)的(值),
#其中[數字]欄位填-1代表倒數第一位,
#其中[數字]欄位可用[數字1:數字2]的寫法,表示從第 數字1位 開始取到第 數字2位 之前不包含第數字2位的值 的所有值,
#而數字1/數字2不填代表從最前開始取/取到最後,
#以上列表規則與字串[]相通

#[列表1].extend([列表2]) //將[列表1]尾端接上[列表2](列表)
#[列表].append([值]) //將[列表]尾端接上[值](列表)
#[列表].insert([index],[值]) //在[列表]的第[index]位插入[值](列表)
#[列表].remove([值]) //將[列表]中的[值]刪除(列表)
#[列表].clear() //清空[列表](列表)
#[列表].pop() //移除[列表]的最後一個值(列表)
#[列表].sort() //將[列表]由小到大做排列(列表)
#[列表].reverse() //將[列表]反轉(列表)
#[列表].index([值]) //將[列表]中[值]所在的位置做回傳(int)
#[列表].count([值]) //計算[列表]中有幾個[值]並回傳(int)
#len([列表]) //回傳[列表]長度(int)

#[變數]=([值],[值],[值],[值],...) //元組tuple,
#元組一旦宣告完後就不可再做更改,
#其餘跟列表一樣

#def [函式名稱](參數名稱,參數名稱,參數名稱,...): //創建函式
def test():
    print("hi")
    print("2")
    return 3 #沒寫return則預設return None
#函式內容前面一定要留白(tab)

#if [條件式]: //if ,類似函式規則
#   [執行語句]
#elif [條件式]:
#   [執行語句]
#else:
#   [執行語句]
#==,<,>,<=,>=,and,or,not([變數]),!=

#[變數]={[鍵]:[值],[鍵]:[值],[鍵]:[值],:,....}//字典dictionary,
#類似自定義index名稱的陣列

#while [條件式]://while ,結構類似函式跟if
#+=

#for [變數] in [字串或列表]: //for ,結構類似函式跟if跟while
#    [執行語句]
#每次執行依序將[字串或列表]拆成單個元素給到[變數]內,
#for [變數] in range([數字]):
#    [執行語句]
#每次執行依序將0~[數字]-1給到[變數]內,
#for [變數] in range([數字1],[數字2]):
#    [執行語句]
#每次執行依序將[數字1]~[數字2]-1給到[變數]內

#[變數]=[[[值],[值],[值],...],[[值],[值],[值],...],...] //2維列表list(類似陣列)

#for [變數1] in [2維列表]:
#   for [變數2] in [變數1]:
#//依序存取[2維列表]內的值(存到[變數2]裡面)
hi=[[1,2],[3,4]]
for ro in hi:
   for co in ro:
       print(co)

#//檔案讀取寫入
#[變數]=open("檔案名稱",mode="開啟模式")
#檔案名稱:絕對路徑或檔名.副檔名
#開啟模式:r,w,a (跟C一樣)
#[檔案變數].read() //讀取全部內容
#[檔案變數].readline() //讀取單行內容
#[檔案變數].readlines() //將每行內容依序放到列表內
#[檔案變數].close() //關檔
#for [變數] in [檔案變數]://一行一行讀取檔案內容到[變數]內
#[檔案變數].write([字串]) //清空後寫檔
#[變數]=open("檔案名稱",mode="開啟模式",encoding="編碼方式") //可控制編碼方式
#[變數]=open("檔案名稱",mode="開啟模式",encoding="utf-8") //utf-8才支援中文
#with open("檔案名稱",mode="開啟模式",encoding="編碼方式") as [變數]:
#   [執行語句]
#//不用close的寫法

#import [檔案名稱]//模組module ,
#引入名稱為[檔案名稱]的檔案,
#可使用其內的變數跟函式
#######不同檔案的東西都要做引入
#import [模組名稱] as [名稱] //類似typedef
#from [模組名稱] import [模組內變數或函式] //只引入[模組名稱]中的[模組內變數或函式]
#//存取方式
#[模組名稱].變數
#[模組名稱].函式()
#import sys
#sys.path

#pip 套件管理工具,指令請輸入在terminal
#pip install numpy
#import numpy

#//類別class
#class [名稱]:
#   def __init__(self,[變數1],[變數2],[變數3],...):
#       self.[變數1]=[變數1]
#       self.[變數2]=[變數2]
#       self.[變數3]=[變數3]
#       self...
#   def [函式名稱](self,,,...):
#       [執行語句]
#   //需用self.[變數]存取沒傳入的變數
#   
#//物件object
#[變數]=[類別函式]([參數],...)

#//繼承inheritance //跟java差不多
#class [名稱1]([名稱2])://[名稱1]繼承[名稱2]
