from bs4 import BeautifulSoup
import requests
import os
from glob import glob
import sys
import pygame
import time
pygame.init()
pygame.mixer.init()
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clearConsole()

#playMusic()

def playMusic(music_name_in_data_folder):
    folder_path=os.path.dirname(os.path.realpath(sys.argv[0]))
    splicing="data\\"+music_name_in_data_folder
    full_path=os.path.join(folder_path,splicing)
    pygame.mixer.music.load(full_path)
    pygame.mixer.music.play()
    time.sleep(1)
    pygame.mixer.music.stop()


#welcome()

def welcome():
    print(" _________________________")
    print("|                         |")
    print("| [Welcome to Kemono_Bug] |")
    print("|_________________________|")
    print()
    print("Please select service :")
    print("[0] => All Auto")
    print("[1] => Select artist")
    print("[2] => Get subpage id")
    print("[3] => Get img link")
    print("[4] => Download img")
    print("[5] => Delete process file")
    print("[q] => Quit")
    select=input()
    return select

#select_artist_1()

def select_artist_1():
    try:
        print("{select_artist} START.")

        if not os.path.exists("./data"):
            os.mkdir("./data")

        if os.path.isfile("./data\\Artist_List.txt"):
            f = open("./data\\Artist_List.txt","r")
        else:
            print("#####LOAD_ERROR:<Artist_List> in {select_artist}")
            os.system("pause")
            exit()

        IdList=[]
        NameList=[]
        TypeList=[]
        Fanbox_length=int(f.readline().strip())
        Patreon_length=int(f.readline().strip())
        Fantia_length=int(f.readline().strip())

#   [TYPE]_length=int(f.readline().strip())
    
        i=0
        bandonLine=f.readline()
        while i<Fanbox_length:
            bandonLine=f.readline()
            id=f.readline().strip()
            IdList.append(id)
            name=f.readline().strip()
            NameList.append(name)
            type=f.readline().strip()
            TypeList.append(type)
            i+=1
        i=0
        bandonLine=f.readline()
        while i<Patreon_length:
            bandonLine=f.readline()
            id=f.readline().strip()
            IdList.append(id)
            name=f.readline().strip()
            NameList.append(name)
            type=f.readline().strip()
            TypeList.append(type)
            i+=1
        i=0
        bandonLine=f.readline()
        while i<Fantia_length:
            bandonLine=f.readline()
            id=f.readline().strip()
            IdList.append(id)
            name=f.readline().strip()
            NameList.append(name)
            type=f.readline().strip()
            TypeList.append(type)
            i+=1

#      i=0
#      bandonLine=f.readline()
#      while i<[TYPE]_length:
#          bandonLine=f.readline()
#          id=f.readline().strip()
#          IdList.append(id)
#          name=f.readline().strip()
#          NameList.append(name)
#          type=f.readline().strip()
#          TypeList.append(type)
#          i+=1

        f.close()

        if Fanbox_length>0:
            print("---------------Fanbox---------------")
            i=0
            j=0
            while i<Fanbox_length:
                print("["+str(i+1)+"] => "+NameList[i]+", "+IdList[i])
                i+=1
        if Patreon_length>0:
            print("---------------Patreon--------------")
            j=0
            while j<Patreon_length:
                print("["+str(i+1)+"] => "+NameList[i]+", "+IdList[i])
                i+=1
                j+=1
        if Fantia_length>0:
            print("---------------Fantia--------------")
            j=0
            while j<Fantia_length:
                print("["+str(i+1)+"] => "+NameList[i]+", "+IdList[i])
                i+=1
                j+=1

#       if [TYPE]_length>0:
#           print("---------------[TYPE]--------------")
#           j=0
#           while j<[TYPE]_length:
#               print("["+str(i+1)+"] => "+NameList[i]+", "+IdList[i])
#               i+=1
#               j+=1

        print("[q] => Quit")
        ARTIST_ID=""
        ARTIST_NAME=""
        ARTIST_TYPE=""
        selected=0
        while True:
            select=input("Select Artist:")
            i=0
            while i<len(NameList):
                if  select == "q" or select == "Q":
                    print("BYE BYE!")
                    exit("{select_artist} FINISH.")
                if str(i+1) == select:
                    ARTIST_ID=IdList[int(select)-1]
                    ARTIST_NAME=NameList[int(select)-1]
                    ARTIST_TYPE=TypeList[int(select)-1]
                    selected=1
                    break
                i+=1

            if selected==1:
                break
            
            print("Invalid number , Please type again...")

        if os.path.isfile("./data\\Artist_info.txt"):
            os.remove("./data\\Artist_info.txt")

        f = open("./data\\Artist_info.txt","w")
        f.write(ARTIST_ID+"\n")
        f.write(ARTIST_NAME+"\n")
        f.write(ARTIST_TYPE+"\n")
        f.close()

        if os.path.isfile("./data\\subpage_id.txt"):
            os.remove("./data\\subpage_id.txt")

        if os.path.isfile("./data\\img_link_log.txt"):
            os.remove("./data\\img_link_log.txt")

        if os.path.isfile("./data\\download_Log.txt"):
            os.remove("./data\\download_Log.txt")

        L=glob("./data\\*_imgLink.txt")
        i=0
        while i<len(L):
            os.remove(L[i])
            i+=1
        print("{select_artist} FINISH.")

    except:
        print("CRASH IN select_artist_1()...")
        playMusic("fail.wav")
        stop=input("Please press any key to continue...")

    finally:    
        f.close()

#get_subpage_id_2()

def get_subpage_id_2():
    try:
        print("{get_subpage_id} START.")
        #ARTIST####

        if os.path.isfile("./data\\Artist_info.txt"):
            f = open("./data\\Artist_info.txt","r")
            ARTIST_ID=f.readline().strip()
            ARTIST_NAME=f.readline().strip()
            ARTIST_TYPE=f.readline().strip()
        else:
            exit("#####LOAD_ERROR:<ARTIST_info> in {get_subpage_id}")

        f.close()
        #ARTIST####

        #Calculate subpage number & last webpage number & last webpage start at##########################################################
        print("[Calculate subpage number & last webpage number & last webpage start at]...")

        response = requests.get(f"https://kemono.party/"+ARTIST_TYPE+"/user/"+ARTIST_ID+"/")
        soup = BeautifulSoup(response.text, "html.parser")
        titles = soup.find_all("small")
        text=titles[0].getText()
        i = len(text)-1
        while text[i]!="0" and text[i]!="1" and text[i]!="2" and text[i]!="3" and text[i]!="4" and text[i]!="5" and text[i]!="6" and text[i]!="7" and text[i]!="8" and text[i]!="9":
            i-=1
        e=i+1
        while text[i]=="0" or text[i]=="1" or text[i]=="2" or text[i]=="3" or text[i]=="4" or text[i]=="5" or text[i]=="6" or text[i]=="7" or text[i]=="8" or text[i]=="9":
            i-=1
        s=i+1
        i=s
        smaxsubpage = ""
        while i<e:
            smaxsubpage += text[i]
            i+=1
        maxsubpage = int(smaxsubpage)
        lastO = 0
        i = 0
        while lastO+25<maxsubpage:
            lastO+=25
            i+=1
        si=str(i)
        slastO=str(lastO)
        print("[Calculate subpage number & last webpage number & last webpage start at] finish.")
        print("<subpage number> = "+smaxsubpage)
        print("<last webpage number> = "+si)
        print("<last webpage start at> = "+slastO)
        print("...")
        #Calculate subpage number & last webpage number & last webpage start at##########################################################

        #Get all subpage link id##########################################################
        print("[Get all subpage link id]...")

        page=0
        L = []
        i = 0
        printi=0

        f=open("./data\\subpage_id.txt","w")
        while page<=lastO:
            strpage=str(page)
            response = requests.get(f"https://kemono.party/"+ARTIST_TYPE+"/user/"+ARTIST_ID+"/?o="+strpage)
            soup = BeautifulSoup(response.text, "html.parser")
            titles = soup.find_all("article")
            for title in titles:
                L.append(title.get("data-id"))
                f.write(L[i]+"\n")
                print("subpage:"+str(i+1)+",\tid:"+L[i])
                i+=1
            page+=25
        f.close()
        si=str(i)
        print("[Get all subpage link id] finish.")
        print("<subpage link number> = "+si)
        print("...")
        #allSubpage##########################################################
        print("{get_subpage_id} FINISH.")

    except:
        print("CRASH IN get_subpage_id_2()...")
        playMusic("fail.wav")
        stop=input("Please press any key to continue...")

    finally:    
        f.close()


#get_img_link_3()

def get_img_link_3():
    try:
        print("{get_img_link} START.")
        #ARTIST####

        if os.path.isfile("./data\\Artist_info.txt"):
            f = open("./data\\Artist_info.txt","r")
        else:
            exit("#####LOAD_ERROR:<ARTIST_info> in {get_img_link}")


        ARTIST_ID=f.readline().strip()
        ARTIST_NAME=f.readline().strip()
        ARTIST_TYPE=f.readline().strip()
        f.close()
        #ARTIST####

        #subpage_id####
        subpageIdList=[]
        if os.path.isfile("./data\\subpage_id.txt"):
            f = open("./data\\subpage_id.txt","r")
        else:
            exit("#####LOAD_ERROR:<subpage_id> in {get_img_link}")

        i=0
        subpage_id=f.readline().strip()
        while subpage_id!="":
            subpageIdList.append(subpage_id)
            subpage_id=f.readline().strip()
        f.close()
        #subpage_id####

        #getImgLink##########################################################
        print("[Get image link]...")

        i = 0
        j = 0
        R = []
        data_id = []
        R_length = []
        sum=0
        realSum=0
        preLogNumber=0
        delnum=0
        idLen=0
        delNumNotEqualTo2=[]
        if os.path.isfile("./data\\img_link_log.txt"):
            f=open("./data\\img_link_log.txt","r")
            preLogi=f.readline().strip()
            i=0
            while preLogi!="":
                R_length.append(preLogi)
                while i<int(preLogi):
                    preLog=f.readline().strip()
                    R.append(preLog)
                    realSum+=1
                    i+=1
                i=0
                preLogNumber+=1
                preLogi=f.readline().strip()
            f.close()

        f=open("./data\\img_link_log.txt","a")
        i=preLogNumber
        while i<len(subpageIdList):
            if i==preLogNumber:
                print("get start at subpage:"+str(preLogNumber+1))
            R_length_length = 0
            idLen = 0
            delnum = 0
            response = requests.get(f"https://kemono.party/"+ARTIST_TYPE+"/user/"+ARTIST_ID+"/post/"+subpageIdList[i])
            data_id.append(subpageIdList[i])
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("img",loading="lazy")
            sum+=len(results)
            GoodText=[]
            for title in results:
                testtext=title.get("src")
                if testtext.find("thumbnail") !=-1:
                    GoodText.append(testtext)
                    idLen+=1
                else:
                    delnum+=1
            #if delnum!=2:
                #delNumNotEqualTo2.append(data_id[i])
            R_length.append(idLen)
            f.write(str(idLen)+"\n")
            j=0
            while j<idLen:
                R.append(GoodText[j])
                f.write(GoodText[j]+"\n")
                j+=1
            realSum+=idLen
            print("subpage:"+str(i+1)+",\timg number:"+str(R_length[i])+",\tsum:"+str(realSum))
            i+=1

        f.close()
        #expected_value =sum-(len(subpageIdList)*2)

        i=0
        sum=0
        while i<len(R_length):
            sum+=int(R_length[i])
            i+=1

        print("[Get image link] finish.")
        if len(subpageIdList)==len(R_length):
            print("data id number check: CORRECT")
        else:
            exit("data id number check: ERROR, len(subpageIdList)!=len(R_length), ("+str(len(subpageIdList))+","+str(len(R_length))+")")
        print("<data id number> = "+str(len(subpageIdList)))

        if len(R)==sum:
            print("image link number check: CORRECT")
        else:
            exit("image link number check: ERROR, len(R)!=sum, ("+str(len(R))+","+str(sum)+")")
        print("<image link number> = "+str(sum))

        #print("EXPECTED VALUE :"+str(expected_value))
        print("...")
        #getImgLink##########################################################
        #os.system("pause")
        #write file##########################################################
        print("[Write file]...")

        f=open("./data\\"+ARTIST_NAME+"_imgLink.txt","w")

        f.write(str(len(R))+"\n")
        f.write(str(len(subpageIdList))+"\n")
        f.write(str(len(R_length))+"\n")

        i=0
        while i<len(R):
            f.write(str(R[i])+"\n")
            i+=1

        i=0
        while i<len(subpageIdList):
            f.write(str(subpageIdList[i])+"\n")
            i+=1

        i=0
        while i<len(R_length):
            f.write(str(R_length[i])+"\n")
            i+=1

        f.close()
        print("[Write file] finsh.")
        #write file##########################################################
        print("{get_img_link} FINISH.")

    except:
        print("CRASH IN get_img_link_3()...")
        playMusic("fail.wav")
        stop=input("Please press any key to continue...")

    finally:    
        f.close()

#download_img_4()

def download_img_4():
    try:
        print("{download_img} START.")

        if os.path.isfile("./data\\Artist_info.txt"):
            f = open("./data\\Artist_info.txt","r")
        else:
            exit("#####LOAD_ERROR:<ARTIST_info> in {download_img}")

        ARTIST_ID=f.readline().strip()
        ARTIST_NAME=f.readline().strip()
        ARTIST_TYPE=f.readline().strip()
        f.close()
        print("[Load img link file]...")

        imgLinkList = []
        dataIdList = []
        dataIdLengthList = []

        if os.path.isfile("./data\\"+ARTIST_NAME+"_imgLink.txt"):
            f = open("./data\\"+ARTIST_NAME+"_imgLink.txt","r")
        else:
            exit("#####LOAD_ERROR:<"+ARTIST_NAME+"_imgLink> in {download_img}")


        imgLinkNumber = f.readline().strip()
        dataIdNumber = f.readline().strip()
        dataIdLengthNumber = f.readline().strip()


        i=0
        while i<int(imgLinkNumber):
            line=f.readline().strip()
            imgLinkList.append(line)
            i+=1

        i=0
        while i<int(dataIdNumber):
            line=f.readline().strip()
            dataIdList.append(line)
            i+=1

        i=0
        while i<int(dataIdLengthNumber):
            line=f.readline().strip()
            dataIdLengthList.append(int(line))
            i+=1
        f.close()

        print("[Load img link file] finish.")
        print("<img link number> = "+str(len(imgLinkList)))
        print("<data id number> ="+str(len(dataIdList)))
        print("<data id length number> ="+str(len(dataIdLengthList)))
        ###########################################

        print("[Download image]...")

        if not os.path.isfile("./data\\download_Log.txt"):
            f = open("./data\\download_Log.txt","w")
            f.write("0")
            f.close()

        f = open("./data\\download_Log.txt","r")
        currentNumber=int(f.readline().strip())
        f.close()
        i=0
        j=0
        k=0
        is_currentNumber=0
        downloadnumber = currentNumber
        while i<len(dataIdLengthList):
            while j<dataIdLengthList[i]:
                if k==currentNumber:
                    is_currentNumber=1
                    break
                j+=1
                k+=1
            if is_currentNumber==1:
                break
            i+=1
            j=0

        if not os.path.exists("./images"):
            os.mkdir("./images")

        if not os.path.exists("./images/"+ARTIST_NAME+"_"+ARTIST_TYPE):
            os.mkdir("./images/"+ARTIST_NAME+"_"+ARTIST_TYPE)
        if i<len(dataIdLengthList):
            print("Download strat at id:"+str(dataIdList[i])+": "+str(j+1)+"/"+str(dataIdLengthList[i])+"...")
        while i<len(dataIdLengthList):
            while j<dataIdLengthList[i]:
                print("downloading img in id "+str(dataIdList[i])+": "+str(j+1)+"/"+str(dataIdLengthList[i])+"...")
                print("https://kemono.party"+imgLinkList[k]+" ("+str(k+1)+"/"+str(len(imgLinkList))+")\n")
                jpgName = dataIdList[i]+"_"+str(j)+".jpg"
                f = open("./images/"+ARTIST_NAME+"_"+ARTIST_TYPE+"\\"+jpgName,'wb')
                response = requests.get('https://kemono.party'+imgLinkList[k])
                f.write(response.content)
                f.close()
                f = open("./data\\download_Log.txt","w")
                downloadnumber+=1
                f.write(str(downloadnumber))
                f.close()
                j+=1
                k+=1
            i+=1
            j=0

        print("[Download image] finish.")
        print("<download number> = "+str(downloadnumber))
        print("{download_img} FINISH.")

    except:
        print("CRASH IN download_img_4()...")
        playMusic("fail.wav")
        stop=input("Please press any key to continue...")

    finally:    
        f.close()
        return ARTIST_NAME+"_"+ARTIST_TYPE


#delete_process_file_5()

def delete_process_file_5():
    try:
        print("{delete_process_file} START.")
        if os.path.isfile("./data\\Artist_info.txt"):
            os.remove("./data\\Artist_info.txt")

        if os.path.isfile("./data\\subpage_id.txt"):
            os.remove("./data\\subpage_id.txt")

        if os.path.isfile("./data\\img_link_log.txt"):
            os.remove("./data\\img_link_log.txt")

        if os.path.isfile("./data\\download_Log.txt"):
            os.remove("./data\\download_Log.txt")

        L=glob("./data\\*_imgLink.txt")
        i=0
        while i<len(L):
            os.remove(L[i])       
            i+=1
        print("{delete_process_file} FINISH.")

    except:
        print("CRASH IN delete_process_file_5()...")
        playMusic("fail.wav")
        stop=input("Please press any key to continue...")
