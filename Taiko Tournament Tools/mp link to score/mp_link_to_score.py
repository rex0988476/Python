from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
f=open('setup.txt','r')
set_up=f.readlines()
f.close()
player_link=set_up[0].split(',')[1][:-1]
write_out_file_name=f"mp score.txt"
maps_diff_link_scores=[]
i=1
while i<len(set_up):
	set_up_list=set_up[i].split(',')
	maps_diff_link_scores.append([set_up_list[0],set_up_list[1],[]])
	if maps_diff_link_scores[i-1][1][-1]=='\n':
		maps_diff_link_scores[i-1][1]=maps_diff_link_scores[i-1][1][:-1]
	i+=1

f=open('mplink.txt','r')
mps=f.readlines()
match_link=mps[0]
if match_link[-1]=='\n':
	match_link=match_link[:-1]

def link_to_index(link):
	global maps_diff_link_scores
	i=0
	while i<len(maps_diff_link_scores):
		if maps_diff_link_scores[i][1]==link:
			return i
		i+=1
	return -1

def get_eng_name(name):
	eng_name=""
	i=0
	while i<len(name):
		if name[i].isdigit():
			break
		else:
			eng_name+=name[i]
		i+=1
	return eng_name

chrome = webdriver.Chrome('./chromedriver')
chrome.get(match_link)
time.sleep(2)
while True:
	try:
		show_more_btn=chrome.find_element(value="show-more-link",by=By.CLASS_NAME)
		show_more_btn.click()
		time.sleep(2)
		chrome.execute_script("window.scrollTo(0,0)")
		time.sleep(1)
	except:
		break
time.sleep(2)

soup = BeautifulSoup(chrome.page_source, "html.parser")
titles=soup.find_all("a",class_="mp-history-game__header")
print('len',len(titles))
i=0
while i<len(titles):
	link=titles[i].get('href')
	index=link_to_index(link)
	if index!=-1:
		t0=titles[i].find_next_siblings("div")
		st0=BeautifulSoup(str(t0), "html.parser")
		s=st0.find_all('div',class_="mp-history-player-score__main")
		j=0
		while j<len(s):
			ssoup=BeautifulSoup(str(s[j]),"html.parser")
			ss=ssoup.find('div',class_="mp-history-player-score__info-box mp-history-player-score__info-box--user")
			sssoup=BeautifulSoup(str(ss),"html.parser")
			sss=sssoup.find_all('a',href=f"{player_link}")
			if len(sss)==1:
				score=ssoup.find('div',class_="mp-history-player-score__info-box mp-history-player-score__info-box--stats")
				scoresoup=BeautifulSoup(str(score),"html.parser")
				sscore=scoresoup.find('span',class_="mp-history-player-score__stat-number mp-history-player-score__stat-number--large")
				sscores=sscore.getText()
				scoress=""
				k=0
				while k<len(sscores):
					if sscores[k].isdigit():
						scoress+=sscores[k]
					k+=1

				if get_eng_name(maps_diff_link_scores[index][0]) in ['FM','TB']:
					mods_name=""
					has_hd=False
					has_hr=False
					mod_hd=scoresoup.find_all('div',title="Hidden")
					mod_hr=scoresoup.find_all('div',title="Hard Rock")
					if len(mod_hd)>0:
						has_hd=True
					if len(mod_hr)>0:
						has_hr=True
					if has_hd and has_hr:
						mods_name='HDHR'
					elif has_hd:
						mods_name='HD'
					elif has_hr:
						mods_name='HR'
					else:
						mods_name='NM'
					scoress = mods_name+','+scoress

				maps_diff_link_scores[index][2].append(scoress)
				print(f'{i+1}/{len(titles)}:{maps_diff_link_scores[index][0]} {scoress}')
				
				break
			j+=1
		if j==len(s):
			print(f"{i+1}/{len(titles)}:didn't play.")
	else:
		print(f'{i+1}/{len(titles)}:not target map.')
	i+=1


i=0
while i<len(maps_diff_link_scores):
	if get_eng_name(maps_diff_link_scores[i][0]) in ['FM','TB']:
		nm_list=[]
		hd_list=[]
		hr_list=[]
		hdhr_list=[]
		k=0
		while k<len(maps_diff_link_scores[i][2]):
			mod=maps_diff_link_scores[i][2][k].split(',')[0]
			if mod=='NM':
				nm_list.append(maps_diff_link_scores[i][2][k].split(',')[1])
			elif mod=='HD':
				hd_list.append(maps_diff_link_scores[i][2][k].split(',')[1])
			elif mod=='HR':
				hr_list.append(maps_diff_link_scores[i][2][k].split(',')[1])
			elif mod=='HDHR':
				hdhr_list.append(maps_diff_link_scores[i][2][k].split(',')[1])
			k+=1
		del maps_diff_link_scores[i][2]
		maps_diff_link_scores[i].append([nm_list,hd_list,hr_list,hdhr_list])
	i+=1


print("===============================")
fmtbmods=['NM','HD','HR','HDHR']
i=0
while i<len(maps_diff_link_scores):
	print(maps_diff_link_scores[i][0])
	if not get_eng_name(maps_diff_link_scores[i][0]) in ['FM','TB']:
		j=0
		while j<len(maps_diff_link_scores[i][2]):
			print(maps_diff_link_scores[i][2][j])
			j+=1
	else:
		k=0
		while k<4:
			print(fmtbmods[k])
			j=0
			while j<len(maps_diff_link_scores[i][2][k]):
				print(maps_diff_link_scores[i][2][k][j])
				j+=1
			k+=1
		
	i+=1
#write out
f=open(write_out_file_name,'w')
i=0
while i<len(maps_diff_link_scores):
	f.write(maps_diff_link_scores[i][0]+'\n')
	if not get_eng_name(maps_diff_link_scores[i][0]) in ['FM','TB']:
		if len(maps_diff_link_scores[i][2])>0:
			j=0
			while j<len(maps_diff_link_scores[i][2])-1:
				f.write(maps_diff_link_scores[i][2][j]+',')
				j+=1
			f.write(maps_diff_link_scores[i][2][j]+'\n')
		else:
			f.write('\n')
	else:
		k=0
		while k<4:
			f.write(fmtbmods[k]+',')
			if len(maps_diff_link_scores[i][2][k])>0:
				j=0
				while j<len(maps_diff_link_scores[i][2][k])-1:
					f.write(maps_diff_link_scores[i][2][k][j]+',')
					j+=1
				f.write(maps_diff_link_scores[i][2][k][j]+'\n')
			else:
				f.write('\n')
			k+=1
	i+=1
f.close()

