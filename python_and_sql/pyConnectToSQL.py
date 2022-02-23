#cursor.execute("") //執行sql語句函式
#變數 = cursor.fetchall() //接收所有sql回傳資料
from sqlite3 import connect
import mysql.connector

connection = mysql.connector.connect(host='localhost',#創建連線
                                    port='3306',
                                    user='root',
                                    password='hsieh17')
#                                   database='company' ) #可先預設要使用的資料庫

cursor = connection.cursor()#開始使用

#創建資料庫
#cursor.execute("CREATE DATABASE `qq`;")
# #創建名為qq的資料庫 #雙引號內可使用sql指令 #重複創建會出錯

#取得所有資料庫名稱
cursor.execute("SHOW DATABASES;")
records = cursor.fetchall()#取出所有sql回傳的資料(列表)
for r in records:#印出取得的所有資料庫名稱
    print(r)

#選擇資料庫
cursor.execute("USE `company`;")

#創建表格
#cursor.execute("CREATE TABLE `qqq`(`qqqq` INT);")

#取得部門表格所有資料
cursor.execute("SELECT * FROM `branch`;")
records = cursor.fetchall()
for r in records:
    print(r)

#新增資料
#cursor.execute("INSERT INTO `branch` VALUES(5,`qq`,NULL)")

#修改資料
#cursor.execute("UPDATE `branch` SET `manager_id` = NULL WHERE `branch_id` = 4;")

#刪除資料
#cursor.execute("DELETE FROM `branch` WHERE `branch_id` = 5;")


cursor.close()#關閉使用
connection.commit()#提交 有動到資料的都需要打這行才會生效
connection.close()#關閉連線