from soupsieve import select
import Kemono_Bug

select = Kemono_Bug.welcome()
while True:
    if select == "0":
        Kemono_Bug.select_artist_1()
        Kemono_Bug.get_subpage_id_2()
        Kemono_Bug.get_img_link_3()
        Kemono_Bug.download_img_4()
        Kemono_Bug.delete_process_file_5()
        break

    elif select == "1":
        Kemono_Bug.select_artist_1()
        break
    
    elif select == "2":
        Kemono_Bug.get_subpage_id_2()
        break
    
    elif select == "3":
        Kemono_Bug.get_img_link_3()
        break
    
    elif select == "4":
        Kemono_Bug.download_img_4()
        break
    
    elif select == "5":
        Kemono_Bug.delete_process_file_5()
        break

    elif select == "q" or select == "Q":
        exit("BYE BYE!")

    else:
        print("Invalid input...")
        select = input()



