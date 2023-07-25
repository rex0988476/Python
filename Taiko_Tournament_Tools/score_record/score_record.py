from PyQt5 import QtGui, QtWidgets, QtCore
import sys
import os
import threading
import statistics

class MyWidget(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Taiko tournament score form')
		self.width_=1600
		self.height_=900
		self.resize(self.width_, self.height_)
		self.style()
		self.ui()
		self.diffs=[]#{name,label_name,map_link_and_name,change_btn,highest,lowest,average,showall,all_scores,addnew,delete}
		#row:label_name,(map_name),link,highest,lowest,average,showall,addnew,delete}
		self.diff_name=['NM','HD','HR','DT','FM','TB']
		self.save_name=""

	def style(self):
		self.style_box = '''
			background:#1a1a1a;
			border:1px solid #000;
			font-size:20px;
			color:white;
			font-family:Verdana;
			border-color:#1a1a1a;
			margin:1px
		'''
		self.style_nm = '''
			color:#F0F0F0;
		'''
		self.style_hd = '''
			color:#FFFF37;
		'''
		self.style_hr = '''
			color:#FF0000;
		'''
		self.style_dt = '''
			color:#B15BFF;
		'''
		self.style_fm = '''
			color:#53FF53;
		'''
		self.style_tb = '''
			color:#4DFFFF;
		'''
		self.style_gold = '''
			background:#FFD700;
			color:black;
		'''
		self.style_silver = '''
			background:#c0c0c0;
			color:black;
		'''
		self.style_copper = '''
			background:#b87333;
			color:black;
		'''
		self.style_gold_bad = '''
			background:#750000;
			color:black;
		'''
		self.style_silver_bad = '''
			background:#FF5151;
			color:black;
		'''
		self.style_copper_bad = '''
			background:#FFB5B5;
			color:black;
		'''
		self.style_show_all_scores = '''
			font-size:30px;
		'''
		self.style_btn = '''
			QPushButton{
				background:#1f538d;
				border:1px solid #000;
				border-radius:10px;
				padding:5px;
			}
			QPushButton:pressed{
				background:#a5bad1;
			}
			QPushButton:disabled{
				background:#a5bad1;
				color:#999999;
			}
		'''

	def ui(self):
		self.main_box = QtWidgets.QWidget(self)
		self.main_box.setGeometry(0,0,600,800)
		self.main_box.setStyleSheet(self.style_box)

		self.main_layout = QtWidgets.QFormLayout(self.main_box)

		self.form_create_btn=QtWidgets.QPushButton(self)
		self.form_create_btn.setText('Create new form')
		self.form_create_btn.setStyleSheet(self.style_btn)
		self.form_create_btn.clicked.connect(self.create_new_form)

		self.form_open_btn=QtWidgets.QPushButton(self)
		self.form_open_btn.setText('Open form')
		self.form_open_btn.setStyleSheet(self.style_btn)
		self.form_open_btn.clicked.connect(self.open_form)

		self.main_layout.addRow(self.form_create_btn,self.form_open_btn)

	def create_new_form(self,diffs=[],is_new=True):
		
		if is_new:
			self.diffs=[]
			self.save_name==""
			self.setWindowTitle('Taiko tournament score form')
		i=0
		while i<self.main_layout.rowCount()-1:
			self.main_layout.removeRow(1)

		#create row
		self.diff_create_btn=QtWidgets.QPushButton(self)
		self.diff_create_btn.setText('Add diff')
		self.diff_create_btn.setStyleSheet(self.style_btn)
		self.diff_create_btn.clicked.connect(self.create_new_diff)

		self.diff_type_box=QtWidgets.QComboBox(self)
		self.diff_type_box.addItems(self.diff_name)

		self.main_layout.addRow(self.diff_create_btn,self.diff_type_box)
		#info row
		self.info_widget=QtWidgets.QWidget()
		self.info_layout=QtWidgets.QHBoxLayout(self.info_widget)

		self.info_label_diff=QtWidgets.QLabel(self)
		self.info_label_diff.setText('Mod')
		self.info_label_map=QtWidgets.QLabel(self)
		self.info_label_map.setText('Map')
		self.info_label_high=QtWidgets.QLabel(self)
		self.info_label_high.setText('Highest')
		self.info_label_low=QtWidgets.QLabel(self)
		self.info_label_low.setText('Lowest')
		self.info_label_avg=QtWidgets.QLabel(self)
		self.info_label_avg.setText('Average')
		self.info_label_play_count=QtWidgets.QLabel(self)
		self.info_label_play_count.setText('Play count')
		self.info_layout.addWidget(self.info_label_diff)
		self.info_layout.addWidget(self.info_label_map)
		self.info_layout.addWidget(self.info_label_high)
		self.info_layout.addWidget(self.info_label_low)
		self.info_layout.addWidget(self.info_label_avg)
		self.info_layout.addWidget(self.info_label_play_count)

		self.main_layout.addRow(self.info_widget)


		#change map link and name
		self.label_change_map_link_and_name_btn=QtWidgets.QPushButton(self)
		self.label_change_map_link_and_name_btn.setText('Change map link and name')
		self.label_change_map_link_and_name_btn.setStyleSheet(self.style_btn)
		self.label_change_map_link_and_name_btn.clicked.connect(self.change_map_link_and_name_window)

		self.current_change_diff_type_box=QtWidgets.QComboBox(self)
		#create new scores row
		self.add_new_score_btn=QtWidgets.QPushButton(self)
		self.add_new_score_btn.setText('Add new score')
		self.add_new_score_btn.setStyleSheet(self.style_btn)
		self.add_new_score_btn.clicked.connect(lambda:self.add_new_scores_window(self.get_eng_name(self.current_create_score_diff_type_box.currentText())))

		self.current_create_score_diff_type_box=QtWidgets.QComboBox(self)
		#show all scores row
		self.all_scores_btn=QtWidgets.QPushButton(self)
		self.all_scores_btn.setText('Show all scores')
		self.all_scores_btn.setStyleSheet(self.style_btn)
		self.all_scores_btn.clicked.connect(self.show_all_scores_window)

		self.current_show_diff_type_box=QtWidgets.QComboBox(self)
		#delete row
		self.diff_delete_btn=QtWidgets.QPushButton(self)
		self.diff_delete_btn.setText('Delete diff')
		self.diff_delete_btn.setStyleSheet(self.style_btn)
		self.diff_delete_btn.clicked.connect(self.delete_diff)

		self.current_del_diff_type_box=QtWidgets.QComboBox(self)
		#save form
		self.save_btn=QtWidgets.QPushButton(self)
		self.save_btn.setText('Save form')
		self.save_btn.setStyleSheet(self.style_btn)
		if is_new:
			self.save_btn.clicked.connect(self.save_window)
		else:
			self.save_btn.clicked.connect(lambda:self.save(self.save_name))

		if is_new:
			i=0
			while i<len(self.diff_name):
				label_name=QtWidgets.QLabel(self)
				label_name.setText(f"{self.diff_name[i]}1")
				if self.diff_name[i]=='NM':
					label_name.setStyleSheet(self.style_nm)
				if self.diff_name[i]=='HD':
					label_name.setStyleSheet(self.style_hd)
				if self.diff_name[i]=='HR':
					label_name.setStyleSheet(self.style_hr)
				if self.diff_name[i]=='DT':
					label_name.setStyleSheet(self.style_dt)
				if self.diff_name[i]=='FM':
					label_name.setStyleSheet(self.style_fm)
				if self.diff_name[i]=='TB':
					label_name.setStyleSheet(self.style_tb)

				label_map_link_and_name=QtWidgets.QLabel(self)
				label_map_link_and_name.setOpenExternalLinks(True)

				label_highest_score=QtWidgets.QLabel(self)
				label_highest_score.setText('-')
				label_lowest_score=QtWidgets.QLabel(self)
				label_lowest_score.setText('-')
				label_average_score=QtWidgets.QLabel(self)
				label_average_score.setText('-')
				label_play_count=QtWidgets.QLabel(self)
				label_play_count.setText('0')

				widget = QtWidgets.QWidget()
				layout = QtWidgets.QHBoxLayout(widget)
				layout.addWidget(label_name)
				layout.addWidget(label_map_link_and_name)
				layout.addWidget(label_highest_score)
				layout.addWidget(label_lowest_score)
				layout.addWidget(label_average_score)
				layout.addWidget(label_play_count)
				#all scores ['all_scores'][{'mods_name':'NM','mods_scores':[1,2,...]}{}{}{}]
				#[{nm [{nm1},{nm2},...]},{hd [{hd1,hd2,...}]}]
				if self.diff_name[i] in ['FM','TB']:
					self.diffs.append({'diff_name':self.diff_name[i],'diffs':[{'num':1,'name':f"{self.diff_name[i]}1",'label_name':label_name,'map_link_and_name':label_map_link_and_name,'highest':label_highest_score,'lowest':label_lowest_score,'average':label_average_score,'mods':'','all_scores':[],'play_count':label_play_count,'widget':widget,'layout':layout}]})
					self.diffs[i]['diffs'][0]['all_scores'].append({'mods_name':'NM','mods_scores':[],'is_first':0})
					self.diffs[i]['diffs'][0]['all_scores'].append({'mods_name':'HD','mods_scores':[],'is_first':0})
					self.diffs[i]['diffs'][0]['all_scores'].append({'mods_name':'HR','mods_scores':[],'is_first':0})
					self.diffs[i]['diffs'][0]['all_scores'].append({'mods_name':'HDHR','mods_scores':[],'is_first':0})
				else:
					self.diffs.append({'diff_name':self.diff_name[i],'diffs':[{'num':1,'name':f"{self.diff_name[i]}1",'label_name':label_name,'map_link_and_name':label_map_link_and_name,'highest':label_highest_score,'lowest':label_lowest_score,'average':label_average_score,'all_scores':[],'play_count':label_play_count,'widget':widget,'layout':layout}]})
				#label_name,map_link_and_name,change_btn,highest,lowest,average,showall,addnew}
				#self.main_layout.addRow(self.diffs[i]['widget'])
				#self.update_current_del_box('add',f"{self.diff_name[i]}1",-1)
				self.update_all_box('add',f"{self.diff_name[i]}1",index=-1)
				i+=1
		else:
			i=0
			while i<len(self.diffs):
				j=0
				while j<len(self.diffs[i]['diffs']):
					self.update_all_box('add',self.diffs[i]['diffs'][j]['name'],index=-1)
					j+=1
				i+=1
			self.count_diff_rank()

		self.scroll_widget = QtWidgets.QWidget()
		self.scroll_layout = QtWidgets.QFormLayout(self.scroll_widget)
		i=0
		while i<len(self.diffs):
			j=0
			while j<len(self.diffs[i]['diffs']):
				self.scroll_layout.addRow(self.diffs[i]['diffs'][j]['widget'])
				j+=1
			i+=1

		self.scroll_area=QtWidgets.QScrollArea(self)

		self.main_layout.addRow(self.scroll_area)
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setWidget(self.scroll_widget)

		self.main_layout.addRow(self.label_change_map_link_and_name_btn,self.current_change_diff_type_box)
		self.main_layout.addRow(self.add_new_score_btn,self.current_create_score_diff_type_box)
		self.main_layout.addRow(self.all_scores_btn,self.current_show_diff_type_box)
		self.main_layout.addRow(self.diff_delete_btn,self.current_del_diff_type_box)
		self.main_layout.addRow(self.save_btn)

	def open_form(self):
		self.file_dialog=QtWidgets.QFileDialog()
		QtWidgets.QFileDialog.setDirectory(self.file_dialog,'./')
		filePath , filterType = self.file_dialog.getOpenFileNames(filter='TXT (*.txt)')  # 選擇檔案對話視窗
		if len(filePath)>0:
			f=open(filePath[0],'r')
			self.save_name=filePath[0].split('/')[-1][:-4]
			print('saven',self.save_name)
			#try:
			#{'num':1,'name':f"{self.diff_name[i]}1",'label_name':label_name,'map_link_and_name':label_map_link_and_name,'highest':label_highest_score,'lowest':label_lowest_score,'average':label_average_score,'all_scores':[],'widget':widget,'layout':layout}
			#難度名稱1,難度名稱2,...
			diffs=f.readline()[:-1]
			diffs_list=diffs.split(',')
			self.diffs=[]
			i=0
			while i<len(diffs_list):
				if not diffs_list[i] in self.diff_name:#check
					print('txt syntax error 1')
					os._exit(0)
				self.diffs.append({'diff_name':diffs_list[i],'diffs':[]})
				i+=1
			#
			s=f.readline()[:-1]
			index=0
			i=0
			while s!="":
				if s=="#":
					#print('s=#')
					index+=1
					i=0
				else:
					diffs1=s
					diffs2=f.readline()[:-1]
					#難度名稱x的每筆資料diffs: num,name,map_name,map_link,highest,lowest,average
					diffs1_list=diffs1.split(',')
					if len(diffs1_list)!=8:#check
						print('txt syntax error 2')
						os._exit(0)
					num=int(diffs1_list[0])
					name=diffs1_list[1]
					map_name=diffs1_list[2]
					map_link=diffs1_list[3]
					highest=diffs1_list[4]
					lowest=diffs1_list[5]
					average=diffs1_list[6]
					play_count=diffs1_list[7]
					label_name=QtWidgets.QLabel(self)
					label_name.setText(name)
					if self.diffs[index]['diff_name']=='NM':
						label_name.setStyleSheet(self.style_nm)
					if self.diffs[index]['diff_name']=='HD':
						label_name.setStyleSheet(self.style_hd)
					if self.diffs[index]['diff_name']=='HR':
						label_name.setStyleSheet(self.style_hr)
					if self.diffs[index]['diff_name']=='DT':
						label_name.setStyleSheet(self.style_dt)
					if self.diffs[index]['diff_name']=='FM':
						label_name.setStyleSheet(self.style_fm)
					if self.diffs[index]['diff_name']=='TB':
						label_name.setStyleSheet(self.style_tb)
					label_map_link_and_name=QtWidgets.QLabel(self)
					label_map_link_and_name.setOpenExternalLinks(True)
					if map_name!=' 'and map_link!=' ':
						label_map_link_and_name.setText(self.get_hyper_link(map_name,map_link))
					label_highest_score=QtWidgets.QLabel(self)
					label_highest_score.setText(highest)
					label_lowest_score=QtWidgets.QLabel(self)
					label_lowest_score.setText(lowest)
					label_average_score=QtWidgets.QLabel(self)
					label_average_score.setText(average)
					label_play_count=QtWidgets.QLabel(self)
					label_play_count.setText(play_count)
					widget = QtWidgets.QWidget()
					layout = QtWidgets.QHBoxLayout(widget)
					layout.addWidget(label_name)
					layout.addWidget(label_map_link_and_name)
					layout.addWidget(label_highest_score)
					layout.addWidget(label_lowest_score)
					layout.addWidget(label_average_score)
					layout.addWidget(label_play_count)
					#{'num':1,'name':f"{self.diff_name[i]}1",'label_name':label_name,'map_link_and_name':label_map_link_and_name,'highest':label_highest_score,'lowest':label_lowest_score,'average':label_average_score,'all_scores':[],'widget':widget,'layout':layout}
					if self.diffs[index]['diff_name'] in ['FM','TB']:
						self.diffs[index]['diffs'].append({'num':num,'name':name,'label_name':label_name,'map_link_and_name':label_map_link_and_name,'highest':label_highest_score,'lowest':label_lowest_score,'average':label_average_score,'mods':'','all_scores':[],'play_count':label_play_count,'widget':widget,'layout':layout})
						self.diffs[index]['diffs'][i]['all_scores'].append({'mods_name':'NM','mods_scores':[],'is_first':0})
						self.diffs[index]['diffs'][i]['all_scores'].append({'mods_name':'HD','mods_scores':[],'is_first':0})
						self.diffs[index]['diffs'][i]['all_scores'].append({'mods_name':'HR','mods_scores':[],'is_first':0})
						self.diffs[index]['diffs'][i]['all_scores'].append({'mods_name':'HDHR','mods_scores':[],'is_first':0})
					else:
						self.diffs[index]['diffs'].append({'num':num,'name':name,'label_name':label_name,'map_link_and_name':label_map_link_and_name,'highest':label_highest_score,'lowest':label_lowest_score,'average':label_average_score,'all_scores':[],'play_count':label_play_count,'widget':widget,'layout':layout})
					#all_scores1,all_scores2,...
					if not(self.diffs[index]['diff_name'] in ['FM','TB']):
						if diffs2!="":
							diffs2_list=diffs2.split(',')
							#print('diff2',diffs2_list)
							#print(self.diffs)
							#os._exit(0)
							j=0
							while j<len(diffs2_list):
								#print('i',i,'j',j)
								self.diffs[index]['diffs'][i]['all_scores'].append(int(diffs2_list[j]))
								j+=1
					else:
						j=0
						while j<4:
							if j!=0:
								diffs2=f.readline()[:-1]
							if diffs2!="":
								diffs2_list=diffs2.split(',')
								#is_first=diffs2_list[-1]
								#del diffs2_list[-1]
								#print('diff2',diffs2_list)
								#print(self.diffs)
								#os._exit(0)
								k=0
								while k<len(diffs2_list):
									#print('i',i,'j',j)
									self.diffs[index]['diffs'][i]['all_scores'][j]['mods_scores'].append(int(diffs2_list[k]))
									k+=1
								#self.diffs[index]['diffs'][i]['all_scores'][j]['is_first']=int(is_first)
								#if int(is_first)==1:
								#	self.diffs[index]['diffs'][i]['mods']=self.diffs[index]['diffs'][i]['all_scores'][j]['mods_name']
							j+=1
					i+=1
				s=f.readline()[:-1]
				
			f.close()
			#except Exception as e:
			#	print('txt syntax error 0')
			#	print(e)
			#	os._exit(0)
			############### init ###############
			self.setWindowTitle(self.save_name)
			self.update_score()
			self.create_new_form(diffs=self.diffs,is_new=False)
	
	#def update_fm_tb_mods_name(self):
	#	i=0
	#	while i<len(self.diffs[self.diff_name_to_index('FM')]['diffs']):
	#		j=0
	#		while j<len(self.diffs[self.diff_name_to_index('FM')]['diffs'][i]['all_scores']):
	#			j+=1
	#		i+=1

	def create_new_diff(self):
		num=0
		last_index=0
		if self.diff_type_box.currentText()=='NM':
			label_name=QtWidgets.QLabel(self)
			num,last_index=self.count_name_num_and_last_index('NM')
			label_name.setText(f"NM{num}")
			label_name.setStyleSheet(self.style_nm)
		elif self.diff_type_box.currentText()=='HD':
			label_name=QtWidgets.QLabel(self)
			num,last_index=self.count_name_num_and_last_index('HD')
			label_name.setText(f"HD{num}")
			label_name.setStyleSheet(self.style_hd)
		elif self.diff_type_box.currentText()=='HR':
			label_name=QtWidgets.QLabel(self)
			num,last_index=self.count_name_num_and_last_index('HR')
			label_name.setText(f"HR{num}")
			label_name.setStyleSheet(self.style_hr)
		elif self.diff_type_box.currentText()=='DT':
			label_name=QtWidgets.QLabel(self)
			num,last_index=self.count_name_num_and_last_index('DT')
			label_name.setText(f"DT{num}")
			label_name.setStyleSheet(self.style_dt)
		elif self.diff_type_box.currentText()=='FM':
			label_name=QtWidgets.QLabel(self)
			num,last_index=self.count_name_num_and_last_index('FM')
			label_name.setText(f"FM{num}")
			label_name.setStyleSheet(self.style_fm)
		elif self.diff_type_box.currentText()=='TB':
			label_name=QtWidgets.QLabel(self)
			num,last_index=self.count_name_num_and_last_index('TB')
			label_name.setText(f"TB{num}")
			label_name.setStyleSheet(self.style_tb)
			
		label_map_link_and_name=QtWidgets.QLabel(self)
		label_map_link_and_name.setOpenExternalLinks(True)

		label_highest_score=QtWidgets.QLabel(self)
		label_highest_score.setText('-')
		label_lowest_score=QtWidgets.QLabel(self)
		label_lowest_score.setText('-')
		label_average_score=QtWidgets.QLabel(self)
		label_average_score.setText('-')
		label_play_count=QtWidgets.QLabel(self)
		label_play_count.setText('0')

		widget = QtWidgets.QWidget()
		layout = QtWidgets.QHBoxLayout(widget)
		layout.addWidget(label_name)
		layout.addWidget(label_map_link_and_name)
		layout.addWidget(label_highest_score)
		layout.addWidget(label_lowest_score)
		layout.addWidget(label_average_score)
		layout.addWidget(label_play_count)
		
		#if len(self.diffs)==0:
		#	last_index=0
		if self.diff_type_box.currentText() in ['FM','TB']:
			self.diffs[self.diff_name_to_index(self.diff_type_box.currentText())]['diffs'].insert(last_index,{'num':num,'name':f"{self.diff_type_box.currentText()}{num}",'label_name':label_name,'map_link_and_name':label_map_link_and_name,'highest':label_highest_score,'lowest':label_lowest_score,'average':label_average_score,'mods':'','all_scores':[],'play_count':label_play_count,'widget':widget,'layout':layout})
			self.diffs[self.diff_name_to_index(self.diff_type_box.currentText())]['diffs'][last_index]['all_scores'].append({'mods_name':'NM','mods_scores':[],'is_first':0})
			self.diffs[self.diff_name_to_index(self.diff_type_box.currentText())]['diffs'][last_index]['all_scores'].append({'mods_name':'HD','mods_scores':[],'is_first':0})
			self.diffs[self.diff_name_to_index(self.diff_type_box.currentText())]['diffs'][last_index]['all_scores'].append({'mods_name':'HR','mods_scores':[],'is_first':0})
			self.diffs[self.diff_name_to_index(self.diff_type_box.currentText())]['diffs'][last_index]['all_scores'].append({'mods_name':'HDHR','mods_scores':[],'is_first':0})
		else:
			self.diffs[self.diff_name_to_index(self.diff_type_box.currentText())]['diffs'].insert(last_index,{'num':num,'name':f"{self.diff_type_box.currentText()}{num}",'label_name':label_name,'map_link_and_name':label_map_link_and_name,'highest':label_highest_score,'lowest':label_lowest_score,'average':label_average_score,'all_scores':[],'play_count':label_play_count,'widget':widget,'layout':layout})
		start_index=self.count_diff_start_index_in_dict(self.diff_type_box.currentText())
		#self.diffs.insert(last_index,{'name':f"{self.diff_type_box.currentText()}{num}",'label_name':label_name,'map_link_and_name':label_map_link_and_name,'highest':label_highest_score,'lowest':label_lowest_score,'average':label_average_score,'all_scores':[],'widget':widget,'layout_label':layout})
		#label_name,map_link_and_name,change_btn,highest,lowest,average,showall,addnew}
		self.scroll_layout.insertRow(start_index+last_index,self.diffs[self.diff_name_to_index(self.diff_type_box.currentText())]['diffs'][last_index]['widget'])
		#self.update_current_del_box('add',f"{self.diff_type_box.currentText()}{num}",start_index+last_index)
		self.update_all_box('add',f"{self.diff_type_box.currentText()}{num}",index=start_index+last_index)

		#self.print_diffs()
		#print('---')

	def diff_name_to_index(self,diffname):
		i=0
		while i<len(self.diff_name):
			if self.diff_name[i]==diffname:
				return i
			i+=1

	def diffs_name_to_index(self,diffsname):
		i=0
		while i<len(self.diffs[self.diff_name_to_index(self.get_eng_name(diffsname))]['diffs']):
			if self.diffs[self.diff_name_to_index(self.get_eng_name(diffsname))]['diffs'][i]['name']==diffsname:
				return i
			i+=1

	def print_diffs(self):
		i=0
		while i<len(self.diffs):
			j=0
			while j<len(self.diffs[i]['diffs']):
				print(self.diffs[i]['diffs'][j]['name'])
				j+=1
			i+=1

	def count_name_num_and_last_index(self,name):
		name_num=0
		last_index=0
		#name_num
		num_l=[]
		index_l=[]
		i=0
		while i<len(self.diffs):
			if self.diffs[i]['diff_name']==name:
				j=0
				while j<len(self.diffs[i]['diffs']):
					index_l.append(j)
					num_l.append(self.diffs[i]['diffs'][j]['num'])
					j+=1
			i+=1
		if len(num_l)>0:
			#print(num_l)
			i=1
			while i<num_l[-1]:
				if not (i in num_l):
					name_num=i
					i=0
					while i<len(num_l):
						if num_l[i]>name_num:
							break
						i+=1
					last_index=index_l[i]
					break
				i+=1
		if name_num==0:
			name_num=len(num_l)+1
			last_index=len(num_l)

		#print(name_num,last_index)
		return name_num,last_index

	def count_diff_start_index_in_dict(self,diffname):
		i=0
		count=0
		while self.diff_name[i]!=diffname:
			count+=len(self.diffs[i]['diffs'])
			i+=1
		return count

	def change_map_link_and_name_window(self):
		self.ui_link_and_name=QtWidgets.QWidget()
		self.ui_link_and_name.setWindowTitle(f'Change map name and link [{self.current_change_diff_type_box.currentText()}]')
		self.ui_link_and_name.setStyleSheet(self.style_box)
		self.ui_link_and_name.setGeometry(self.x()+int(self.width()/2)-500,self.y()+int(self.height()/2)-75,1000,150)
		
		self.link_and_name_layout = QtWidgets.QFormLayout(self.ui_link_and_name)
		#
		self.map_name_label=QtWidgets.QLabel(self.ui_link_and_name)
		self.map_name_label.setText('Map name:')

		self.map_name_line_edit=QtWidgets.QLineEdit(self.ui_link_and_name)
		#
		self.map_link_label=QtWidgets.QLabel(self.ui_link_and_name)
		self.map_link_label.setText('Map url:')

		self.map_link_line_edit=QtWidgets.QLineEdit(self.ui_link_and_name)
		#
		self.map_change_btn=QtWidgets.QPushButton(self.ui_link_and_name)
		self.map_change_btn.setText('Change')
		self.map_change_btn.setStyleSheet(self.style_btn)
		self.map_change_btn.clicked.connect(lambda:self.destroy_and_update_change_map_window('change'))

		self.map_cancel_btn=QtWidgets.QPushButton(self.ui_link_and_name)
		self.map_cancel_btn.setText('Cancel')
		self.map_cancel_btn.setStyleSheet(self.style_btn)
		self.map_cancel_btn.clicked.connect(lambda:self.destroy_and_update_change_map_window('cancel'))
		#
		self.link_and_name_layout.addRow(self.map_name_label,self.map_name_line_edit)
		self.link_and_name_layout.addRow(self.map_link_label,self.map_link_line_edit)
		self.link_and_name_layout.addRow(self.map_cancel_btn,self.map_change_btn)
		self.ui_link_and_name.show()

	def destroy_and_update_change_map_window(self,type_):
		eng_name=self.get_eng_name(self.current_change_diff_type_box.currentText())

		if type_=='change' and self.map_name_line_edit.text()!="" and self.map_link_line_edit.text()!="":
			map_name=""
			map_link=""
			i=0
			while i<len(self.map_name_line_edit.text()):
				if not self.map_name_line_edit.text()[i] in [',','\n']:
					map_name+=self.map_name_line_edit.text()[i]
				i+=1
			i=0
			while i<len(self.map_link_line_edit.text()):
				if not self.map_link_line_edit.text()[i] in [',','\n']:
					map_link+=self.map_link_line_edit.text()[i]
				i+=1
			i=0
			while i<len(self.diffs):
				if self.diffs[i]['diff_name']==eng_name:
					j=0
					while j<len(self.diffs[i]['diffs']):
						if self.diffs[i]['diffs'][j]['name']==self.current_change_diff_type_box.currentText():
							self.diffs[i]['diffs'][j]['map_link_and_name'].setText(self.get_hyper_link(map_name,map_link))
							break
						j+=1
				i+=1
			self.ui_link_and_name.close()
		elif type_=='cancel':
			self.ui_link_and_name.close()        

	def add_new_scores_window(self,diffname):
		self.ui_add_new_scores=QtWidgets.QWidget()
		self.ui_add_new_scores.setWindowTitle(f'Add new score [{self.current_create_score_diff_type_box.currentText()}]')
		self.ui_add_new_scores.setStyleSheet(self.style_box)

		self.add_new_scores_layout = QtWidgets.QFormLayout(self.ui_add_new_scores)
		if diffname=='FM' or diffname=='TB':
			self.ui_add_new_scores.setGeometry(self.x()+int(self.width()/2)-400,self.y()+int(self.height()/2)-75,800,150)
			self.fmtb_mod_label=QtWidgets.QLabel(self.ui_add_new_scores)
			self.fmtb_mod_label.setText('Mods:')
			self.fmtb_combo_box=QtWidgets.QComboBox(self.ui_add_new_scores)
			self.fmtb_combo_box.addItems(['NM','HD','HR','HDHR'])
			self.add_new_scores_layout.addRow(self.fmtb_mod_label,self.fmtb_combo_box)
		else:
			self.ui_add_new_scores.setGeometry(self.x()+int(self.width()/2)-400,self.y()+int(self.height()/2)-50,800,100) 
		
		#
		self.new_scores_label=QtWidgets.QLabel(self.ui_add_new_scores)
		self.new_scores_label.setText('New score:')

		self.new_scores_line_edit=QtWidgets.QLineEdit(self.ui_add_new_scores)
		#
		self.add_new_scores_btn=QtWidgets.QPushButton(self.ui_add_new_scores)
		self.add_new_scores_btn.setText('Add')
		self.add_new_scores_btn.setStyleSheet(self.style_btn)
		self.add_new_scores_btn.clicked.connect(lambda:self.destroy_and_update_add_new_score_window('add'))

		self.add_new_scores_cancel_btn=QtWidgets.QPushButton(self.ui_add_new_scores)
		self.add_new_scores_cancel_btn.setText('Cancel')
		self.add_new_scores_cancel_btn.setStyleSheet(self.style_btn)
		self.add_new_scores_cancel_btn.clicked.connect(lambda:self.destroy_and_update_add_new_score_window('cancel'))
		#
		self.add_new_scores_layout.addRow(self.new_scores_label,self.new_scores_line_edit)
		self.add_new_scores_layout.addRow(self.add_new_scores_cancel_btn,self.add_new_scores_btn)
		self.ui_add_new_scores.show()

	def destroy_and_update_add_new_score_window(self,type_):
		if type_=='add' and self.new_scores_line_edit.text().isdigit() and int(self.new_scores_line_edit.text())>=0:
			diffs_index=self.diffs_name_to_index(self.current_create_score_diff_type_box.currentText())
			if not self.get_eng_name(self.current_create_score_diff_type_box.currentText()) in ['FM','TB']:
				if self.get_eng_name(self.current_create_score_diff_type_box.currentText())=='NM' and int(self.new_scores_line_edit.text())<=1000000:
					index=self.diff_name_to_index('NM')
				elif self.get_eng_name(self.current_create_score_diff_type_box.currentText())=='HD' and int(self.new_scores_line_edit.text())<=1060000:
					index=self.diff_name_to_index('HD')
				elif self.get_eng_name(self.current_create_score_diff_type_box.currentText())=='HR' and int(self.new_scores_line_edit.text())<=1060000:
					index=self.diff_name_to_index('HR')
				elif self.get_eng_name(self.current_create_score_diff_type_box.currentText())=='DT' and int(self.new_scores_line_edit.text())<=1120000:
					index=self.diff_name_to_index('DT')
				self.diffs[index]['diffs'][diffs_index]['all_scores'].append(int(self.new_scores_line_edit.text()))
			else:
				if self.get_eng_name(self.current_create_score_diff_type_box.currentText())=='FM':
					index=self.diff_name_to_index('FM')
				elif self.get_eng_name(self.current_create_score_diff_type_box.currentText())=='TB':
					index=self.diff_name_to_index('TB')
				if self.fmtb_combo_box.currentText()=='NM':
					self.diffs[index]['diffs'][diffs_index]['all_scores'][0]['mods_scores'].append(int(self.new_scores_line_edit.text()))
				elif self.fmtb_combo_box.currentText()=='HD':
					self.diffs[index]['diffs'][diffs_index]['all_scores'][1]['mods_scores'].append(int(self.new_scores_line_edit.text()))
				elif self.fmtb_combo_box.currentText()=='HR':
					self.diffs[index]['diffs'][diffs_index]['all_scores'][2]['mods_scores'].append(int(self.new_scores_line_edit.text()))
				elif self.fmtb_combo_box.currentText()=='HDHR':
					self.diffs[index]['diffs'][diffs_index]['all_scores'][3]['mods_scores'].append(int(self.new_scores_line_edit.text()))
			self.update_score(index,diffs_index)
			self.count_diff_rank()
		elif type_=='cancel':
			pass
		self.ui_add_new_scores.close()

	def update_score(self,diff_index=-1,diff2_index=-1):
		if diff_index==-1 and diff2_index==-1:
			i=0
			while i<len(self.diffs):
				j=0
				while j<len(self.diffs[i]['diffs']):
					if not(self.diffs[i]['diff_name'] in ['FM','TB']):
						if len(self.diffs[i]['diffs'][j]['all_scores'])>0:
							self.diffs[i]['diffs'][j]['all_scores'].sort(reverse=True)
							max_=self.diffs[i]['diffs'][j]['all_scores'][0]
							min_=self.diffs[i]['diffs'][j]['all_scores'][-1]
							mean_=statistics.mean(self.diffs[i]['diffs'][j]['all_scores'])
							self.diffs[i]['diffs'][j]['highest'].setText(str(int(max_)))
							self.diffs[i]['diffs'][j]['lowest'].setText(str(int(min_)))
							self.diffs[i]['diffs'][j]['average'].setText(str(int(mean_)))
							self.diffs[i]['diffs'][j]['play_count'].setText(str(len(self.diffs[i]['diffs'][j]['all_scores'])))
					else:
						max_nm=-1
						min_nm=-1
						mean_nm=-1
						max_hd=-1
						min_hd=-1
						mean_hd=-1
						max_hr=-1
						min_hr=-1
						mean_hr=-1
						max_hdhr=-1
						min_hdhr=-1
						mean_hdhr=-1
						nm_rank=[]
						hd_rank=[]
						hr_rank=[]
						hdhr_rank=[]
						if len(self.diffs[i]['diffs'][j]['all_scores'][0]['mods_scores'])>0:
							self.diffs[i]['diffs'][j]['all_scores'][0]['mods_scores'].sort(reverse=True)
							max_nm=self.diffs[i]['diffs'][j]['all_scores'][0]['mods_scores'][0]
							min_nm=self.diffs[i]['diffs'][j]['all_scores'][0]['mods_scores'][-1]
							mean_nm=statistics.mean(self.diffs[i]['diffs'][j]['all_scores'][0]['mods_scores'])
						if len(self.diffs[i]['diffs'][j]['all_scores'][1]['mods_scores'])>0:
							self.diffs[i]['diffs'][j]['all_scores'][1]['mods_scores'].sort(reverse=True)
							max_hd=self.diffs[i]['diffs'][j]['all_scores'][1]['mods_scores'][0]
							min_hd=self.diffs[i]['diffs'][j]['all_scores'][1]['mods_scores'][-1]
							mean_hd=statistics.mean(self.diffs[i]['diffs'][j]['all_scores'][1]['mods_scores'])
						if len(self.diffs[i]['diffs'][j]['all_scores'][2]['mods_scores'])>0:
							self.diffs[i]['diffs'][j]['all_scores'][2]['mods_scores'].sort(reverse=True)
							max_hr=self.diffs[i]['diffs'][j]['all_scores'][2]['mods_scores'][0]
							min_hr=self.diffs[i]['diffs'][j]['all_scores'][2]['mods_scores'][-1]
							mean_hr=statistics.mean(self.diffs[i]['diffs'][j]['all_scores'][2]['mods_scores'])
						if len(self.diffs[i]['diffs'][j]['all_scores'][3]['mods_scores'])>0:
							self.diffs[i]['diffs'][j]['all_scores'][3]['mods_scores'].sort(reverse=True)
							max_hdhr=self.diffs[i]['diffs'][j]['all_scores'][3]['mods_scores'][0]
							min_hdhr=self.diffs[i]['diffs'][j]['all_scores'][3]['mods_scores'][-1]
							mean_hdhr=statistics.mean(self.diffs[i]['diffs'][j]['all_scores'][3]['mods_scores'])
						#max
						max_list=[{'name':'NM','score':max_nm},{'name':'HD','score':max_hd},{'name':'HR','score':max_hr},{'name':'HDHR','score':max_hdhr}]
						k=0
						while k<len(max_list):
							l=0
							while l<k:
								if max_list[l]['score']<max_list[k]['score']:
									t={}
									t['name']=max_list[l]['name']
									t['score']=max_list[l]['score']
									max_list[l]['name']=max_list[k]['name']
									max_list[l]['score']=max_list[k]['score']
									max_list[k]['name']=t['name']
									max_list[k]['score']=t['score']
								l+=1
							k+=1
						k=0
						while k<len(max_list):
							if max_list[k]['name']=='NM':
								nm_rank.append(k)
							elif max_list[k]['name']=='HD':
								hd_rank.append(k)
							elif max_list[k]['name']=='HR':
								hr_rank.append(k)
							elif max_list[k]['name']=='HDHR':
								hdhr_rank.append(k)
							k+=1
						#min
						min_list=[{'name':'NM','score':min_nm},{'name':'HD','score':min_hd},{'name':'HR','score':min_hr},{'name':'HDHR','score':min_hdhr}]
						k=0
						while k<len(min_list):
							l=0
							while l<k:
								if min_list[l]['score']<min_list[k]['score']:
									t={}
									t['name']=min_list[l]['name']
									t['score']=min_list[l]['score']
									min_list[l]['name']=min_list[k]['name']
									min_list[l]['score']=min_list[k]['score']
									min_list[k]['name']=t['name']
									min_list[k]['score']=t['score']
								l+=1
							k+=1
						k=0
						while k<len(min_list):
							if min_list[k]['name']=='NM':
								nm_rank.append(k)
							elif min_list[k]['name']=='HD':
								hd_rank.append(k)
							elif min_list[k]['name']=='HR':
								hr_rank.append(k)
							elif min_list[k]['name']=='HDHR':
								hdhr_rank.append(k)
							k+=1
						#mean
						mean_list=[{'name':'NM','score':mean_nm},{'name':'HD','score':mean_hd},{'name':'HR','score':mean_hr},{'name':'HDHR','score':mean_hdhr}]
						k=0
						while k<len(mean_list):
							l=0
							while l<k:
								if mean_list[l]['score']<mean_list[k]['score']:
									t={}
									t['name']=mean_list[l]['name']
									t['score']=mean_list[l]['score']
									mean_list[l]['name']=mean_list[k]['name']
									mean_list[l]['score']=mean_list[k]['score']
									mean_list[k]['name']=t['name']
									mean_list[k]['score']=t['score']
								l+=1
							k+=1
						k=0
						while k<len(mean_list):
							if mean_list[k]['name']=='NM':
								nm_rank.append(k)
							elif mean_list[k]['name']=='HD':
								hd_rank.append(k)
							elif mean_list[k]['name']=='HR':
								hr_rank.append(k)
							elif mean_list[k]['name']=='HDHR':
								hdhr_rank.append(k)
							k+=1
						#
						nm_mean_rank=statistics.mean(nm_rank)
						hd_mean_rank=statistics.mean(hd_rank)
						hr_mean_rank=statistics.mean(hr_rank)
						hdhr_mean_rank=statistics.mean(hdhr_rank)
						print('mr:',nm_rank,hd_rank,hr_rank,hdhr_rank)
						#total
						total_rank_list=[{'name':'NM','score':nm_mean_rank},{'name':'HD','score':hd_mean_rank},{'name':'HR','score':hr_mean_rank},{'name':'HDHR','score':hdhr_mean_rank}]
						k=0
						while k<len(total_rank_list):
							l=0
							while l<k:
								if total_rank_list[l]['score']>total_rank_list[k]['score']:
									t={}
									t['name']=total_rank_list[l]['name']
									t['score']=total_rank_list[l]['score']
									total_rank_list[l]['name']=total_rank_list[k]['name']
									total_rank_list[l]['score']=total_rank_list[k]['score']
									total_rank_list[k]['name']=t['name']
									total_rank_list[k]['score']=t['score']
								l+=1
							k+=1
						#
						total_first_rank_name=total_rank_list[0]['name']
						play_count=0
						if total_first_rank_name=='NM':
							total_first_rank_highest=max_nm
							total_first_rank_lowest=min_nm
							total_first_rank_average=mean_nm
							play_count=len(self.diffs[i]['diffs'][j]['all_scores'][0]['mods_scores'])
							self.diffs[i]['diffs'][j]['mods']='NM'
							self.diffs[i]['diffs'][j]['all_scores'][0]['is_first']=1
							self.diffs[i]['diffs'][j]['all_scores'][1]['is_first']=0
							self.diffs[i]['diffs'][j]['all_scores'][2]['is_first']=0
							self.diffs[i]['diffs'][j]['all_scores'][3]['is_first']=0
						elif total_first_rank_name=='HD':
							total_first_rank_highest=max_hd
							total_first_rank_lowest=min_hd
							total_first_rank_average=mean_hd
							play_count=len(self.diffs[i]['diffs'][j]['all_scores'][1]['mods_scores'])
							self.diffs[i]['diffs'][j]['mods']='HD'
							self.diffs[i]['diffs'][j]['all_scores'][0]['is_first']=0
							self.diffs[i]['diffs'][j]['all_scores'][1]['is_first']=1
							self.diffs[i]['diffs'][j]['all_scores'][2]['is_first']=0
							self.diffs[i]['diffs'][j]['all_scores'][3]['is_first']=0
						elif total_first_rank_name=='HR':
							total_first_rank_highest=max_hr
							total_first_rank_lowest=min_hr
							total_first_rank_average=mean_hr
							play_count=len(self.diffs[i]['diffs'][j]['all_scores'][2]['mods_scores'])
							self.diffs[i]['diffs'][j]['mods']='HR'
							self.diffs[i]['diffs'][j]['all_scores'][0]['is_first']=0
							self.diffs[i]['diffs'][j]['all_scores'][1]['is_first']=0
							self.diffs[i]['diffs'][j]['all_scores'][2]['is_first']=1
							self.diffs[i]['diffs'][j]['all_scores'][3]['is_first']=0
						elif total_first_rank_name=='HDHR':
							total_first_rank_highest=max_hdhr
							total_first_rank_lowest=min_hdhr
							total_first_rank_average=mean_hdhr
							play_count=len(self.diffs[i]['diffs'][j]['all_scores'][3]['mods_scores'])
							self.diffs[i]['diffs'][j]['mods']='HDHR'
							self.diffs[i]['diffs'][j]['all_scores'][0]['is_first']=0
							self.diffs[i]['diffs'][j]['all_scores'][1]['is_first']=0
							self.diffs[i]['diffs'][j]['all_scores'][2]['is_first']=0
							self.diffs[i]['diffs'][j]['all_scores'][3]['is_first']=1
						if int(total_first_rank_highest)==-1 and int(total_first_rank_lowest)==-1 and int(total_first_rank_average)==-1:
							self.diffs[i]['diffs'][j]['highest'].setText('-')
							self.diffs[i]['diffs'][j]['lowest'].setText('-')
							self.diffs[i]['diffs'][j]['average'].setText('-')
						else:
							self.diffs[i]['diffs'][j]['highest'].setText(str(int(total_first_rank_highest)))
							self.diffs[i]['diffs'][j]['lowest'].setText(str(int(total_first_rank_lowest)))
							self.diffs[i]['diffs'][j]['average'].setText(str(int(total_first_rank_average)))
						self.diffs[i]['diffs'][j]['play_count'].setText(str(play_count))
					j+=1
				i+=1
		
		else:
			if not(self.diffs[diff_index]['diff_name'] in ['FM','TB']):
				self.diffs[diff_index]['diffs'][diff2_index]['all_scores'].sort(reverse=True)
				max_=self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][0]
				min_=self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][-1]
				mean_=statistics.mean(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'])
				self.diffs[diff_index]['diffs'][diff2_index]['highest'].setText(str(int(max_)))
				self.diffs[diff_index]['diffs'][diff2_index]['lowest'].setText(str(int(min_)))
				self.diffs[diff_index]['diffs'][diff2_index]['average'].setText(str(int(mean_)))
				self.diffs[diff_index]['diffs'][diff2_index]['play_count'].setText(str(len(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'])))
			else:
				max_nm=-1
				min_nm=-1
				mean_nm=-1
				max_hd=-1
				min_hd=-1
				mean_hd=-1
				max_hr=-1
				min_hr=-1
				mean_hr=-1
				max_hdhr=-1
				min_hdhr=-1
				mean_hdhr=-1
				nm_rank=[]
				hd_rank=[]
				hr_rank=[]
				hdhr_rank=[]
				if len(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][0]['mods_scores'])>0:
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][0]['mods_scores'].sort(reverse=True)
					max_nm=self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][0]['mods_scores'][0]
					min_nm=self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][0]['mods_scores'][-1]
					mean_nm=statistics.mean(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][0]['mods_scores'])
				if len(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][1]['mods_scores'])>0:
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][1]['mods_scores'].sort(reverse=True)
					max_hd=self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][1]['mods_scores'][0]
					min_hd=self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][1]['mods_scores'][-1]
					mean_hd=statistics.mean(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][1]['mods_scores'])
				if len(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][2]['mods_scores'])>0:
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][2]['mods_scores'].sort(reverse=True)
					max_hr=self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][2]['mods_scores'][0]
					min_hr=self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][2]['mods_scores'][-1]
					mean_hr=statistics.mean(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][2]['mods_scores'])
				if len(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][3]['mods_scores'])>0:
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][3]['mods_scores'].sort(reverse=True)
					max_hdhr=self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][3]['mods_scores'][0]
					min_hdhr=self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][3]['mods_scores'][-1]
					mean_hdhr=statistics.mean(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][3]['mods_scores'])
				#max
				max_list=[{'name':'NM','score':max_nm},{'name':'HD','score':max_hd},{'name':'HR','score':max_hr},{'name':'HDHR','score':max_hdhr}]
				print('max:',max_hdhr,max_list[0]['score'],max_list[1]['score'],max_list[2]['score'],max_list[3]['score'])
				k=0
				while k<len(max_list):
					l=0
					while l<k:
						print('e',max_list[l]['name'],max_list[k]['name'])
						if max_list[l]['score']<max_list[k]['score']:
							t={}
							t['name']=max_list[l]['name']
							t['score']=max_list[l]['score']
							max_list[l]['name']=max_list[k]['name']
							max_list[l]['score']=max_list[k]['score']
							max_list[k]['name']=t['name']
							max_list[k]['score']=t['score']
						l+=1
					k+=1
				k=0
				while k<len(max_list):
					if max_list[k]['name']=='NM':
						nm_rank.append(k)
					elif max_list[k]['name']=='HD':
						hd_rank.append(k)
					elif max_list[k]['name']=='HR':
						hr_rank.append(k)
					elif max_list[k]['name']=='HDHR':
						hdhr_rank.append(k)
					k+=1
				#min
				min_list=[{'name':'NM','score':min_nm},{'name':'HD','score':min_hd},{'name':'HR','score':min_hr},{'name':'HDHR','score':min_hdhr}]
				print('min:',min_list[0]['score'],min_list[1]['score'],min_list[2]['score'],min_list[3]['score'])
				k=0
				while k<len(min_list):
					l=0
					while l<k:
						print('e',min_list[l]['name'],min_list[k]['name'])
						if min_list[l]['score']<min_list[k]['score']:
							t={}
							t['name']=min_list[l]['name']
							t['score']=min_list[l]['score']
							min_list[l]['name']=min_list[k]['name']
							min_list[l]['score']=min_list[k]['score']
							min_list[k]['name']=t['name']
							min_list[k]['score']=t['score']
						l+=1
					k+=1
				k=0
				while k<len(min_list):
					if min_list[k]['name']=='NM':
						nm_rank.append(k)
					elif min_list[k]['name']=='HD':
						hd_rank.append(k)
					elif min_list[k]['name']=='HR':
						hr_rank.append(k)
					elif min_list[k]['name']=='HDHR':
						hdhr_rank.append(k)
					k+=1
				#mean
				mean_list=[{'name':'NM','score':mean_nm},{'name':'HD','score':mean_hd},{'name':'HR','score':mean_hr},{'name':'HDHR','score':mean_hdhr}]
				print('mean:',mean_list[0]['score'],mean_list[1]['score'],mean_list[2]['score'],mean_list[3]['score'])
				k=0
				while k<len(mean_list):
					l=0
					while l<k:
						if mean_list[l]['score']<mean_list[k]['score']:
							t={}
							t['name']=mean_list[l]['name']
							t['score']=mean_list[l]['score']
							mean_list[l]['name']=mean_list[k]['name']
							mean_list[l]['score']=mean_list[k]['score']
							mean_list[k]['name']=t['name']
							mean_list[k]['score']=t['score']
						l+=1
					k+=1
				
				k=0
				while k<len(mean_list):
					if mean_list[k]['name']=='NM':
						nm_rank.append(k)
					elif mean_list[k]['name']=='HD':
						hd_rank.append(k)
					elif mean_list[k]['name']=='HR':
						hr_rank.append(k)
					elif mean_list[k]['name']=='HDHR':
						hdhr_rank.append(k)
					k+=1
				#
				nm_mean_rank=statistics.mean(nm_rank)
				hd_mean_rank=statistics.mean(hd_rank)
				hr_mean_rank=statistics.mean(hr_rank)
				hdhr_mean_rank=statistics.mean(hdhr_rank)
				print('mr:',nm_rank,hd_rank,hr_rank,hdhr_rank)
				#print('mr:',nm_mean_rank,hd_mean_rank,hr_mean_rank,hdhr_mean_rank)
				#total
				total_rank_list=[{'name':'NM','score':nm_mean_rank},{'name':'HD','score':hd_mean_rank},{'name':'HR','score':hr_mean_rank},{'name':'HDHR','score':hdhr_mean_rank}]
				k=0
				while k<len(total_rank_list):
					l=0
					while l<k:
						if total_rank_list[l]['score']>total_rank_list[k]['score']:
							t={}
							t['name']=total_rank_list[l]['name']
							t['score']=total_rank_list[l]['score']
							total_rank_list[l]['name']=total_rank_list[k]['name']
							total_rank_list[l]['score']=total_rank_list[k]['score']
							total_rank_list[k]['name']=t['name']
							total_rank_list[k]['score']=t['score']
						l+=1
					k+=1
				#
				total_first_rank_name=total_rank_list[0]['name']
				play_count=0
				if total_first_rank_name=='NM':
					total_first_rank_highest=max_nm
					total_first_rank_lowest=min_nm
					total_first_rank_average=mean_nm
					play_count=len(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][0]['mods_scores'])
					self.diffs[diff_index]['diffs'][diff2_index]['mods']='NM'
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][0]['is_first']=1
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][1]['is_first']=0
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][2]['is_first']=0
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][3]['is_first']=0
				elif total_first_rank_name=='HD':
					total_first_rank_highest=max_hd
					total_first_rank_lowest=min_hd
					total_first_rank_average=mean_hd
					play_count=len(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][1]['mods_scores'])
					self.diffs[diff_index]['diffs'][diff2_index]['mods']='HD'
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][0]['is_first']=0
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][1]['is_first']=1
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][2]['is_first']=0
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][3]['is_first']=0
				elif total_first_rank_name=='HR':
					total_first_rank_highest=max_hr
					total_first_rank_lowest=min_hr
					total_first_rank_average=mean_hr
					play_count=len(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][2]['mods_scores'])
					self.diffs[diff_index]['diffs'][diff2_index]['mods']='HR'
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][0]['is_first']=0
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][1]['is_first']=0
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][2]['is_first']=1
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][3]['is_first']=0
				elif total_first_rank_name=='HDHR':
					total_first_rank_highest=max_hdhr
					total_first_rank_lowest=min_hdhr
					total_first_rank_average=mean_hdhr
					play_count=len(self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][3]['mods_scores'])
					self.diffs[diff_index]['diffs'][diff2_index]['mods']='HDHR'
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][0]['is_first']=0
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][1]['is_first']=0
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][2]['is_first']=0
					self.diffs[diff_index]['diffs'][diff2_index]['all_scores'][3]['is_first']=1
				if int(total_first_rank_highest)==-1 and int(total_first_rank_lowest)==-1 and int(total_first_rank_average)==-1:
					self.diffs[diff_index]['diffs'][diff2_index]['highest'].setText('-')
					self.diffs[diff_index]['diffs'][diff2_index]['lowest'].setText('-')
					self.diffs[diff_index]['diffs'][diff2_index]['average'].setText('-')
				else:
					self.diffs[diff_index]['diffs'][diff2_index]['highest'].setText(str(int(total_first_rank_highest)))
					self.diffs[diff_index]['diffs'][diff2_index]['lowest'].setText(str(int(total_first_rank_lowest)))
					self.diffs[diff_index]['diffs'][diff2_index]['average'].setText(str(int(total_first_rank_average)))
				self.diffs[diff_index]['diffs'][diff2_index]['play_count'].setText(str(play_count))
				 
	def count_diff_rank(self):
		target=['highest','lowest','average']
		l=0
		while l<len(target):
			first_index1=-1
			first_index2=-1
			second_index1=-1
			second_index2=-1
			third_index1=-1
			third_index2=-1
			first_bad_index1=-1
			first_bad_index2=-1
			second_bad_index1=-1
			second_bad_index2=-1
			third_bad_index1=-1
			third_bad_index2=-1
			#gold
			max_=0
			i=0
			while i<len(self.diffs):
				j=0
				while j<len(self.diffs[i]['diffs']):
					self.diffs[i]['diffs'][j][target[l]].setStyleSheet(self.style_box)
					if self.diffs[i]['diffs'][j]['play_count'].text()!='0':
						denominator=0
						if self.diffs[i]['diff_name']=='NM':
							denominator=1000000
						elif self.diffs[i]['diff_name'] in ['HD','HR']:
							denominator=1060000
						elif self.diffs[i]['diff_name']=='DT':
							denominator=1120000
						elif self.diffs[i]['diff_name'] in ['FM','TB']:
							if self.diffs[i]['diffs'][j]['mods']=='NM':
								denominator=1000000
							elif self.diffs[i]['diffs'][j]['mods'] in ['HD','HR']:
								denominator=1060000
							elif self.diffs[i]['diffs'][j]['mods']=='HDHR':
								denominator=1120000
						if int(self.diffs[i]['diffs'][j][target[l]].text())/denominator>=max_:
							max_=int(self.diffs[i]['diffs'][j][target[l]].text())/denominator
							first_index1=i
							first_index2=j
					j+=1
				i+=1
			if first_index1!=-1 and first_index2!=-1:
				self.diffs[first_index1]['diffs'][first_index2][target[l]].setStyleSheet(self.style_gold)
			#silver
			max_=0
			i=0
			while i<len(self.diffs):
				j=0
				while j<len(self.diffs[i]['diffs']):
					if not(i==first_index1 and j==first_index2):
						self.diffs[i]['diffs'][j][target[l]].setStyleSheet(self.style_box)
						if self.diffs[i]['diffs'][j]['play_count'].text()!='0':
							denominator=0
							if self.diffs[i]['diff_name']=='NM':
								denominator=1000000
							elif self.diffs[i]['diff_name'] in ['HD','HR']:
								denominator=1060000
							elif self.diffs[i]['diff_name']=='DT':
								denominator=1120000
							elif self.diffs[i]['diff_name'] in ['FM','TB']:
								if self.diffs[i]['diffs'][j]['mods']=='NM':
									denominator=1000000
								elif self.diffs[i]['diffs'][j]['mods'] in ['HD','HR']:
									denominator=1060000
								elif self.diffs[i]['diffs'][j]['mods']=='HDHR':
									denominator=1120000
							if int(self.diffs[i]['diffs'][j][target[l]].text())/denominator>=max_:
								max_=int(self.diffs[i]['diffs'][j][target[l]].text())/denominator
								second_index1=i
								second_index2=j
					j+=1
				i+=1
			if second_index1!=-1 and second_index2!=-1:
				self.diffs[second_index1]['diffs'][second_index2][target[l]].setStyleSheet(self.style_silver)
			#copper
			max_=0
			i=0
			while i<len(self.diffs):
				j=0
				while j<len(self.diffs[i]['diffs']):
					if (not(i==first_index1 and j==first_index2)) and (not(i==second_index1 and j==second_index2)):
						self.diffs[i]['diffs'][j][target[l]].setStyleSheet(self.style_box)
						if self.diffs[i]['diffs'][j]['play_count'].text()!='0':
							denominator=0
							if self.diffs[i]['diff_name']=='NM':
								denominator=1000000
							elif self.diffs[i]['diff_name'] in ['HD','HR']:
								denominator=1060000
							elif self.diffs[i]['diff_name']=='DT':
								denominator=1120000
							elif self.diffs[i]['diff_name'] in ['FM','TB']:
								if self.diffs[i]['diffs'][j]['mods']=='NM':
									denominator=1000000
								elif self.diffs[i]['diffs'][j]['mods'] in ['HD','HR']:
									denominator=1060000
								elif self.diffs[i]['diffs'][j]['mods']=='HDHR':
									denominator=1120000
							if int(self.diffs[i]['diffs'][j][target[l]].text())/denominator>=max_:
								max_=int(self.diffs[i]['diffs'][j][target[l]].text())/denominator
								third_index1=i
								third_index2=j
					j+=1
				i+=1
			if third_index1!=-1 and third_index2!=-1:
				self.diffs[third_index1]['diffs'][third_index2][target[l]].setStyleSheet(self.style_copper)
			#gold bad
			min_=1
			i=0
			while i<len(self.diffs):
				j=0
				while j<len(self.diffs[i]['diffs']):
					if (not(i==first_index1 and j==first_index2)) and (not(i==second_index1 and j==second_index2)) and (not(i==third_index1 and j==third_index2)):
						self.diffs[i]['diffs'][j][target[l]].setStyleSheet(self.style_box)
						if self.diffs[i]['diffs'][j]['play_count'].text()!='0':
							denominator=0
							if self.diffs[i]['diff_name']=='NM':
								denominator=1000000
							elif self.diffs[i]['diff_name'] in ['HD','HR']:
								denominator=1060000
							elif self.diffs[i]['diff_name']=='DT':
								denominator=1120000
							elif self.diffs[i]['diff_name'] in ['FM','TB']:
								if self.diffs[i]['diffs'][j]['mods']=='NM':
									denominator=1000000
								elif self.diffs[i]['diffs'][j]['mods'] in ['HD','HR']:
									denominator=1060000
								elif self.diffs[i]['diffs'][j]['mods']=='HDHR':
									denominator=1120000
							if int(self.diffs[i]['diffs'][j][target[l]].text())/denominator<=min_:
								min_=int(self.diffs[i]['diffs'][j][target[l]].text())/denominator
								first_bad_index1=i
								first_bad_index2=j
					j+=1
				i+=1
			if first_bad_index1!=-1 and first_bad_index2!=-1:
				self.diffs[first_bad_index1]['diffs'][first_bad_index2][target[l]].setStyleSheet(self.style_gold_bad)
			#silver bad
			min_=1
			i=0
			while i<len(self.diffs):
				j=0
				while j<len(self.diffs[i]['diffs']):
					if (not(i==first_index1 and j==first_index2)) and (not(i==second_index1 and j==second_index2)) and (not(i==third_index1 and j==third_index2)) and (not(i==first_bad_index1 and j==first_bad_index2)):
						self.diffs[i]['diffs'][j][target[l]].setStyleSheet(self.style_box)
						if self.diffs[i]['diffs'][j]['play_count'].text()!='0':
							denominator=0
							if self.diffs[i]['diff_name']=='NM':
								denominator=1000000
							elif self.diffs[i]['diff_name'] in ['HD','HR']:
								denominator=1060000
							elif self.diffs[i]['diff_name']=='DT':
								denominator=1120000
							elif self.diffs[i]['diff_name'] in ['FM','TB']:
								if self.diffs[i]['diffs'][j]['mods']=='NM':
									denominator=1000000
								elif self.diffs[i]['diffs'][j]['mods'] in ['HD','HR']:
									denominator=1060000
								elif self.diffs[i]['diffs'][j]['mods']=='HDHR':
									denominator=1120000
							if int(self.diffs[i]['diffs'][j][target[l]].text())/denominator<=min_:
								min_=int(self.diffs[i]['diffs'][j][target[l]].text())/denominator
								second_bad_index1=i
								second_bad_index2=j
					j+=1
				i+=1
			if second_bad_index1!=-1 and second_bad_index2!=-1:
				self.diffs[second_bad_index1]['diffs'][second_bad_index2][target[l]].setStyleSheet(self.style_silver_bad)
			#copper bad
			min_=1
			i=0
			while i<len(self.diffs):
				j=0
				while j<len(self.diffs[i]['diffs']):
					if (not(i==first_index1 and j==first_index2)) and (not(i==second_index1 and j==second_index2)) and (not(i==third_index1 and j==third_index2)) and (not(i==first_bad_index1 and j==first_bad_index2)) and (not(i==second_bad_index1 and j==second_bad_index2)):
						self.diffs[i]['diffs'][j][target[l]].setStyleSheet(self.style_box)
						if self.diffs[i]['diffs'][j]['play_count'].text()!='0':
							denominator=0
							if self.diffs[i]['diff_name']=='NM':
								denominator=1000000
							elif self.diffs[i]['diff_name'] in ['HD','HR']:
								denominator=1060000
							elif self.diffs[i]['diff_name']=='DT':
								denominator=1120000
							elif self.diffs[i]['diff_name'] in ['FM','TB']:
								if self.diffs[i]['diffs'][j]['mods']=='NM':
									denominator=1000000
								elif self.diffs[i]['diffs'][j]['mods'] in ['HD','HR']:
									denominator=1060000
								elif self.diffs[i]['diffs'][j]['mods']=='HDHR':
									denominator=1120000
							if int(self.diffs[i]['diffs'][j][target[l]].text())/denominator<=min_:
								min_=int(self.diffs[i]['diffs'][j][target[l]].text())/denominator
								third_bad_index1=i
								third_bad_index2=j
					j+=1
				i+=1
			if third_bad_index1!=-1 and third_bad_index2!=-1:
				self.diffs[third_bad_index1]['diffs'][third_bad_index2][target[l]].setStyleSheet(self.style_copper_bad)
			l+=1
		
	def show_all_scores_window(self):
		index1=self.diff_name_to_index(self.get_eng_name(self.current_show_diff_type_box.currentText()))
		index2=self.num_name_to_index(self.current_show_diff_type_box.currentText())

		self.ui_show_all_scores=QtWidgets.QWidget()
		self.ui_show_all_scores.setWindowTitle(f'All scores [{self.current_show_diff_type_box.currentText()}]')
		self.ui_show_all_scores.setStyleSheet(self.style_box)
		self.show_all_scores_layout = QtWidgets.QFormLayout(self.ui_show_all_scores)

		if not (self.get_eng_name(self.current_show_diff_type_box.currentText()) in ['FM','TB']):
			self.ui_show_all_scores.setGeometry(self.x()+int(self.width()/2)-175,self.y()+int(self.height()/2)-400,350,800)
			#
			self.all_scores_scroll_widget = QtWidgets.QWidget()
			self.all_scores_scroll_layout = QtWidgets.QFormLayout(self.all_scores_scroll_widget)
			i=0
			while i<len(self.diffs[index1]['diffs'][index2]['all_scores']):
				score_label=QtWidgets.QLabel(self.ui_show_all_scores)
				score_label.setStyleSheet(self.style_show_all_scores)
				score_label.setText(str(self.diffs[index1]['diffs'][index2]['all_scores'][i]))
				#self.show_all_scores_layout.addRow(score_label)
				self.all_scores_scroll_layout.addRow(score_label)
				i+=1
			#
			self.all_scores_scroll_area=QtWidgets.QScrollArea(self)
			self.show_all_scores_layout.addRow(self.all_scores_scroll_area)
			self.all_scores_scroll_area.setWidgetResizable(True)
			self.all_scores_scroll_area.setWidget(self.all_scores_scroll_widget)
			#
			self.show_all_scores_avg_name_label=QtWidgets.QLabel(self.ui_show_all_scores)
			self.show_all_scores_avg_name_label.setText('Average:')
			self.show_all_scores_avg_num_label=QtWidgets.QLabel(self.ui_show_all_scores)
			self.show_all_scores_avg_num_label.setStyleSheet(self.style_show_all_scores)
			self.show_all_scores_avg_num_label.setText(self.diffs[index1]['diffs'][index2]['average'].text())
			#
			self.show_all_scores_play_count_name_label=QtWidgets.QLabel(self.ui_show_all_scores)
			self.show_all_scores_play_count_name_label.setText('Play count:')
			self.show_all_scores_play_count_num_label=QtWidgets.QLabel(self.ui_show_all_scores)
			self.show_all_scores_play_count_num_label.setStyleSheet(self.style_show_all_scores)
			self.show_all_scores_play_count_num_label.setText(self.diffs[index1]['diffs'][index2]['play_count'].text())
			#
			self.show_all_scores_close_btn=QtWidgets.QPushButton(self.ui_show_all_scores)
			self.show_all_scores_close_btn.setText('Close')
			self.show_all_scores_close_btn.setStyleSheet(self.style_btn)
			self.show_all_scores_close_btn.clicked.connect(lambda:self.ui_show_all_scores.close())
			#
			self.show_all_scores_layout.addRow(self.show_all_scores_avg_name_label,self.show_all_scores_avg_num_label)
			self.show_all_scores_layout.addRow(self.show_all_scores_play_count_name_label,self.show_all_scores_play_count_num_label)
			self.show_all_scores_layout.addRow(self.show_all_scores_close_btn)
			
		else:
			self.ui_show_all_scores.setGeometry(self.x()+int(self.width()/2)-400,self.y()+int(self.height()/2)-400,800,800)
			show_all_scores_nm_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_nm_label.setText('NM')
			if self.diffs[index1]['diffs'][index2]['all_scores'][0]['is_first']==1:
				show_all_scores_nm_label.setStyleSheet(self.style_gold)
			show_all_scores_hd_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hd_label.setText('HD')
			if self.diffs[index1]['diffs'][index2]['all_scores'][1]['is_first']==1:
				show_all_scores_hd_label.setStyleSheet(self.style_gold)
			show_all_scores_hr_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hr_label.setText('HR')
			if self.diffs[index1]['diffs'][index2]['all_scores'][2]['is_first']==1:
				show_all_scores_hr_label.setStyleSheet(self.style_gold)
			show_all_scores_hdhr_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hdhr_label.setText('HDHR')
			if self.diffs[index1]['diffs'][index2]['all_scores'][3]['is_first']==1:
				show_all_scores_hdhr_label.setStyleSheet(self.style_gold)
			
				

			widget = QtWidgets.QWidget()
			layout = QtWidgets.QHBoxLayout(widget)
			layout.addWidget(show_all_scores_nm_label)
			layout.addWidget(show_all_scores_hd_label)
			layout.addWidget(show_all_scores_hr_label)
			layout.addWidget(show_all_scores_hdhr_label)
			self.show_all_scores_layout.addRow(widget)
			#NM
			all_scores_nm_scroll_widget = QtWidgets.QWidget()
			all_scores_nm_scroll_layout = QtWidgets.QFormLayout(all_scores_nm_scroll_widget)
			j=0
			while j<len(self.diffs[index1]['diffs'][index2]['all_scores'][0]['mods_scores']):
				score_label=QtWidgets.QLabel(self.ui_show_all_scores)
				score_label.setStyleSheet(self.style_show_all_scores)
				score_label.setText(str(self.diffs[index1]['diffs'][index2]['all_scores'][0]['mods_scores'][j]))
				all_scores_nm_scroll_layout.addRow(score_label)
				j+=1
				#
			all_scores_nm_scroll_area=QtWidgets.QScrollArea(self)
			
			all_scores_nm_scroll_area.setWidgetResizable(True)
			all_scores_nm_scroll_area.setWidget(all_scores_nm_scroll_widget)
			##
			all_scores_nm_scroll_avg_pc_widget = QtWidgets.QWidget()
			all_scores_nm_scroll_avg_pc_layout = QtWidgets.QFormLayout(all_scores_nm_scroll_avg_pc_widget)
			all_scores_nm_scroll_avg_pc_layout.addRow(all_scores_nm_scroll_area)

			show_all_scores_nm_avg_name_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_nm_avg_name_label.setText('Average:')
			show_all_scores_nm_avg_num_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_nm_avg_num_label.setStyleSheet(self.style_show_all_scores)
			if len(self.diffs[index1]['diffs'][index2]['all_scores'][0]['mods_scores'])>0:
				show_all_scores_nm_avg_num_label.setText(str(int(statistics.mean(self.diffs[index1]['diffs'][index2]['all_scores'][0]['mods_scores']))))
			else:
				show_all_scores_nm_avg_num_label.setText('-')
			#
			show_all_scores_nm_play_count_name_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_nm_play_count_name_label.setText('Play count:')
			show_all_scores_nm_play_count_num_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_nm_play_count_num_label.setStyleSheet(self.style_show_all_scores)
			show_all_scores_nm_play_count_num_label.setText(str(len(self.diffs[index1]['diffs'][index2]['all_scores'][0]['mods_scores'])))

			all_scores_nm_scroll_avg_pc_layout.addRow(show_all_scores_nm_avg_name_label,show_all_scores_nm_avg_num_label)
			all_scores_nm_scroll_avg_pc_layout.addRow(show_all_scores_nm_play_count_name_label,show_all_scores_nm_play_count_num_label)
			#HD
			all_scores_hd_scroll_widget = QtWidgets.QWidget()
			all_scores_hd_scroll_layout = QtWidgets.QFormLayout(all_scores_hd_scroll_widget)
			j=0
			while j<len(self.diffs[index1]['diffs'][index2]['all_scores'][1]['mods_scores']):
				score_label=QtWidgets.QLabel(self.ui_show_all_scores)
				score_label.setStyleSheet(self.style_show_all_scores)
				score_label.setText(str(self.diffs[index1]['diffs'][index2]['all_scores'][1]['mods_scores'][j]))
				all_scores_hd_scroll_layout.addRow(score_label)
				j+=1
				#
			all_scores_hd_scroll_area=QtWidgets.QScrollArea(self)
			
			all_scores_hd_scroll_area.setWidgetResizable(True)
			all_scores_hd_scroll_area.setWidget(all_scores_hd_scroll_widget)
			##
			all_scores_hd_scroll_avg_pc_widget = QtWidgets.QWidget()
			all_scores_hd_scroll_avg_pc_layout = QtWidgets.QFormLayout(all_scores_hd_scroll_avg_pc_widget)
			all_scores_hd_scroll_avg_pc_layout.addRow(all_scores_hd_scroll_area)

			show_all_scores_hd_avg_name_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hd_avg_name_label.setText('Average:')
			show_all_scores_hd_avg_num_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hd_avg_num_label.setStyleSheet(self.style_show_all_scores)
			if len(self.diffs[index1]['diffs'][index2]['all_scores'][1]['mods_scores'])>0:
				show_all_scores_hd_avg_num_label.setText(str(int(statistics.mean(self.diffs[index1]['diffs'][index2]['all_scores'][1]['mods_scores']))))
			else:
				show_all_scores_hd_avg_num_label.setText('-')
			#
			show_all_scores_hd_play_count_name_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hd_play_count_name_label.setText('Play count:')
			show_all_scores_hd_play_count_num_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hd_play_count_num_label.setStyleSheet(self.style_show_all_scores)
			show_all_scores_hd_play_count_num_label.setText(str(len(self.diffs[index1]['diffs'][index2]['all_scores'][1]['mods_scores'])))

			all_scores_hd_scroll_avg_pc_layout.addRow(show_all_scores_hd_avg_name_label,show_all_scores_hd_avg_num_label)
			all_scores_hd_scroll_avg_pc_layout.addRow(show_all_scores_hd_play_count_name_label,show_all_scores_hd_play_count_num_label)

			#HR
			all_scores_hr_scroll_widget = QtWidgets.QWidget()
			all_scores_hr_scroll_layout = QtWidgets.QFormLayout(all_scores_hr_scroll_widget)
			j=0
			while j<len(self.diffs[index1]['diffs'][index2]['all_scores'][2]['mods_scores']):
				score_label=QtWidgets.QLabel(self.ui_show_all_scores)
				score_label.setStyleSheet(self.style_show_all_scores)
				score_label.setText(str(self.diffs[index1]['diffs'][index2]['all_scores'][2]['mods_scores'][j]))
				all_scores_hr_scroll_layout.addRow(score_label)
				j+=1
				#
			all_scores_hr_scroll_area=QtWidgets.QScrollArea(self)
			
			all_scores_hr_scroll_area.setWidgetResizable(True)
			all_scores_hr_scroll_area.setWidget(all_scores_hr_scroll_widget)
			##
			all_scores_hr_scroll_avg_pc_widget = QtWidgets.QWidget()
			all_scores_hr_scroll_avg_pc_layout = QtWidgets.QFormLayout(all_scores_hr_scroll_avg_pc_widget)
			all_scores_hr_scroll_avg_pc_layout.addRow(all_scores_hr_scroll_area)

			show_all_scores_hr_avg_name_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hr_avg_name_label.setText('Average:')
			show_all_scores_hr_avg_num_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hr_avg_num_label.setStyleSheet(self.style_show_all_scores)
			if len(self.diffs[index1]['diffs'][index2]['all_scores'][2]['mods_scores'])>0:
				show_all_scores_hr_avg_num_label.setText(str(int(statistics.mean(self.diffs[index1]['diffs'][index2]['all_scores'][2]['mods_scores']))))
			else:
				show_all_scores_hr_avg_num_label.setText('-')
			#
			show_all_scores_hr_play_count_name_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hr_play_count_name_label.setText('Play count:')
			show_all_scores_hr_play_count_num_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hr_play_count_num_label.setStyleSheet(self.style_show_all_scores)
			show_all_scores_hr_play_count_num_label.setText(str(len(self.diffs[index1]['diffs'][index2]['all_scores'][2]['mods_scores'])))

			all_scores_hr_scroll_avg_pc_layout.addRow(show_all_scores_hr_avg_name_label,show_all_scores_hr_avg_num_label)
			all_scores_hr_scroll_avg_pc_layout.addRow(show_all_scores_hr_play_count_name_label,show_all_scores_hr_play_count_num_label)

			#HDHR
			all_scores_hdhr_scroll_widget = QtWidgets.QWidget()
			all_scores_hdhr_scroll_layout = QtWidgets.QFormLayout(all_scores_hdhr_scroll_widget)
			j=0
			while j<len(self.diffs[index1]['diffs'][index2]['all_scores'][3]['mods_scores']):
				score_label=QtWidgets.QLabel(self.ui_show_all_scores)
				score_label.setStyleSheet(self.style_show_all_scores)
				score_label.setText(str(self.diffs[index1]['diffs'][index2]['all_scores'][3]['mods_scores'][j]))
				all_scores_hdhr_scroll_layout.addRow(score_label)
				j+=1
				#
			all_scores_hdhr_scroll_area=QtWidgets.QScrollArea(self)
			
			all_scores_hdhr_scroll_area.setWidgetResizable(True)
			all_scores_hdhr_scroll_area.setWidget(all_scores_hdhr_scroll_widget)
			##
			all_scores_hdhr_scroll_avg_pc_widget = QtWidgets.QWidget()
			all_scores_hdhr_scroll_avg_pc_layout = QtWidgets.QFormLayout(all_scores_hdhr_scroll_avg_pc_widget)
			all_scores_hdhr_scroll_avg_pc_layout.addRow(all_scores_hdhr_scroll_area)

			show_all_scores_hdhr_avg_name_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hdhr_avg_name_label.setText('Average:')
			show_all_scores_hdhr_avg_num_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hdhr_avg_num_label.setStyleSheet(self.style_show_all_scores)
			if len(self.diffs[index1]['diffs'][index2]['all_scores'][3]['mods_scores'])>0:
				show_all_scores_hdhr_avg_num_label.setText(str(int(statistics.mean(self.diffs[index1]['diffs'][index2]['all_scores'][3]['mods_scores']))))
			else:
				show_all_scores_hdhr_avg_num_label.setText('-')
			#
			show_all_scores_hdhr_play_count_name_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hdhr_play_count_name_label.setText('Play count:')
			show_all_scores_hdhr_play_count_num_label=QtWidgets.QLabel(self.ui_show_all_scores)
			show_all_scores_hdhr_play_count_num_label.setStyleSheet(self.style_show_all_scores)
			show_all_scores_hdhr_play_count_num_label.setText(str(len(self.diffs[index1]['diffs'][index2]['all_scores'][3]['mods_scores'])))

			all_scores_hdhr_scroll_avg_pc_layout.addRow(show_all_scores_hdhr_avg_name_label,show_all_scores_hdhr_avg_num_label)
			all_scores_hdhr_scroll_avg_pc_layout.addRow(show_all_scores_hdhr_play_count_name_label,show_all_scores_hdhr_play_count_num_label)
			#
			all_scores_mods_scroll_area_widget = QtWidgets.QWidget()
			all_scores_mods_scroll_area_layout = QtWidgets.QHBoxLayout(all_scores_mods_scroll_area_widget)
			all_scores_mods_scroll_area_layout.addWidget(all_scores_nm_scroll_avg_pc_widget)
			all_scores_mods_scroll_area_layout.addWidget(all_scores_hd_scroll_avg_pc_widget)
			all_scores_mods_scroll_area_layout.addWidget(all_scores_hr_scroll_avg_pc_widget)
			all_scores_mods_scroll_area_layout.addWidget(all_scores_hdhr_scroll_avg_pc_widget)
			###
			#
			self.show_all_scores_layout.addRow(all_scores_mods_scroll_area_widget)
			#####
			self.show_all_scores_close_btn=QtWidgets.QPushButton(self.ui_show_all_scores)
			self.show_all_scores_close_btn.setText('Close')
			self.show_all_scores_close_btn.setStyleSheet(self.style_btn)
			self.show_all_scores_close_btn.clicked.connect(lambda:self.ui_show_all_scores.close())

			self.show_all_scores_layout.addRow(self.show_all_scores_close_btn)

		self.ui_show_all_scores.show()

	def delete_diff(self):
		eng_name=self.get_eng_name(self.current_del_diff_type_box.currentText())
		#print(self.current_del_diff_type_box.currentText())
		i=0
		while i<len(self.diffs):
			if self.diffs[i]['diff_name']==eng_name:
				j=0
				while j<len(self.diffs[i]['diffs']):
					if self.diffs[i]['diffs'][j]['name']==self.current_del_diff_type_box.currentText():
						start_index=self.count_diff_start_index_in_dict(eng_name)
						self.scroll_layout.removeRow(start_index+j)
						del self.diffs[i]['diffs'][j]
						#self.update_current_del_box('del',self.current_del_diff_type_box.currentText())
						self.update_all_box('del',self.current_del_diff_type_box.currentText(),who='del')
						break
					j+=1
			i+=1

	def get_eng_name(self,name):
		#NM1: return NM
		eng_name=""
		i=0
		while i<len(name):
			if not name[i].isdigit():
				eng_name+=name[i]
				i+=1
			else:
				break
		return eng_name

	def num_name_to_index(self,name):
		i=0
		while i<len(self.diffs[self.diff_name_to_index(self.get_eng_name(name))]['diffs']):
			if self.diffs[self.diff_name_to_index(self.get_eng_name(name))]['diffs'][i]['name']==name:
				return i
			i+=1

	def update_all_box(self,type_,diffname,who='',index=0):
		if who=='del':
			self.update_current_del_box(type_,diffname,index,True)
		else:
			self.update_current_del_box(type_,diffname,index)
		if who=='change':
			self.update_change_box(type_,diffname,index,True)
		else:
			self.update_change_box(type_,diffname,index)
		if who=='create':
			self.update_create_score_box(type_,diffname,index,True)
		else:
			self.update_create_score_box(type_,diffname,index)
		if who=='show':
			self.update_show_box(type_,diffname,index,True)
		else:
			self.update_show_box(type_,diffname,index)
		
	def update_current_del_box(self,type_,diffname,index=0,is_self=False):
		if type_ == 'add':
			if index==-1:
				self.current_del_diff_type_box.addItem(diffname)
			else:
				self.current_del_diff_type_box.insertItem(index,diffname)
		elif type_ == 'del':
			if is_self:
				self.current_del_diff_type_box.removeItem(self.current_del_diff_type_box.currentIndex())
			else:
				self.current_del_diff_type_box.removeItem(self.current_del_diff_type_box.findText(diffname))

	def update_change_box(self,type_,diffname,index=0,is_self=False):
		if type_ == 'add':
			if index==-1:
				self.current_change_diff_type_box.addItem(diffname)
			else:
				self.current_change_diff_type_box.insertItem(index,diffname)
		elif type_ == 'del':
			if is_self:
				self.current_change_diff_type_box.removeItem(self.current_change_diff_type_box.currentIndex())
			else:
				self.current_change_diff_type_box.removeItem(self.current_change_diff_type_box.findText(diffname))

	def update_create_score_box(self,type_,diffname,index=0,is_self=False):
		if type_ == 'add':
			if index==-1:
				self.current_create_score_diff_type_box.addItem(diffname)
			else:
				self.current_create_score_diff_type_box.insertItem(index,diffname)
		elif type_ == 'del':
			if is_self:
				self.current_create_score_diff_type_box.removeItem(self.current_create_score_diff_type_box.currentIndex())
			else:
				self.current_create_score_diff_type_box.removeItem(self.current_create_score_diff_type_box.findText(diffname))

	def update_show_box(self,type_,diffname,index=0,is_self=False):
		if type_ == 'add':
			if index==-1:
				self.current_show_diff_type_box.addItem(diffname)
			else:
				self.current_show_diff_type_box.insertItem(index,diffname)
		elif type_ == 'del':
			if is_self:
				self.current_show_diff_type_box.removeItem(self.current_show_diff_type_box.currentIndex())
			else:
				self.current_show_diff_type_box.removeItem(self.current_show_diff_type_box.findText(diffname))

	def get_hyper_link(self,text,url):
		return f'<a href="{url}" style="color:#ffb61e;font-size:20px;font-family:Microsoft YaHei"><b>{text}</b></a>'
	
	def get_name_and_link(self,url):
		link_end=url.find('"',9)
		link=url[9:link_end]
		name_start=url.find('<b>')+3
		name_end=url.find('</b>')
		name=url[name_start:name_end]
		return name,link

	def save_window(self):
		self.ui_save=QtWidgets.QWidget()
		self.ui_save.setWindowTitle('Save form')
		self.ui_save.setStyleSheet(self.style_box)
		self.ui_save.setGeometry(self.x()+int(self.width()/2)-400,self.y()+int(self.height()/2)-50,800,100)
		
		self.save_form_layout = QtWidgets.QFormLayout(self.ui_save)
		#
		self.form_name_label=QtWidgets.QLabel(self.ui_save)
		self.form_name_label.setText('Form name:')

		self.form_name_line_edit=QtWidgets.QLineEdit(self.ui_save)
		#
		self.save_form_btn=QtWidgets.QPushButton(self.ui_save)
		self.save_form_btn.setText('Save')
		self.save_form_btn.setStyleSheet(self.style_btn)
		self.save_form_btn.clicked.connect(lambda:self.destroy_and_update_save_form_window('save'))

		self.save_form_cancel_btn=QtWidgets.QPushButton(self.ui_save)
		self.save_form_cancel_btn.setText('Cancel')
		self.save_form_cancel_btn.setStyleSheet(self.style_btn)
		self.save_form_cancel_btn.clicked.connect(lambda:self.destroy_and_update_save_form_window('cancel'))
		#
		self.save_form_layout.addRow(self.form_name_label,self.form_name_line_edit)
		self.save_form_layout.addRow(self.save_form_cancel_btn,self.save_form_btn)
		self.ui_save.show()

	def destroy_and_update_save_form_window(self,type_):
		all_files=os.listdir('./')
		if type_=='save' and self.form_name_line_edit.text() != "":
			#if not (self.form_name_line_edit.text()+'.txt' in all_files):
			#    self.save(self.form_name_line_edit.text())
			#    self.save_name=self.form_name_line_edit.text()
			#    self.ui_save.close()
			self.save(self.form_name_line_edit.text())
			self.save_name=self.form_name_line_edit.text()
			self.save_btn.clicked.disconnect()
			self.save_btn.clicked.connect(lambda:self.save(self.save_name))
			self.ui_save.close()
		elif type_=='cancel':
			self.ui_save.close()

	def save(self,filename):
		#syntax:
		#難度名稱1,難度名稱2,...
		#難度名稱1的每筆資料diffs: num,name,map_name,map_link,highest,lowest,average
		#all_scores1,all_scores2,...
		#...
		##
		#難度名稱2的每筆資料diffs: num,name,map_name,map_link,highest,lowest,average
		#all_scores1,all_scores2,...
		#...
		##
		#...
		print('savename',filename)
		f=open(f"{filename}.txt","w")
		#難度名稱1,難度名稱2,...
		s=""
		i=0
		while i<len(self.diffs):
			s+=f"{self.diffs[i]['diff_name']},"
			i+=1
		s=s[:-1]
		f.write(s+'\n')
		#難度名稱x的每筆資料
		i=0
		while i<len(self.diffs):
			j=0
			while j<len(self.diffs[i]['diffs']):
				f.write(str(self.diffs[i]['diffs'][j]['num'])+',')
				f.write(self.diffs[i]['diffs'][j]['name']+',')
				name,link=self.get_name_and_link(self.diffs[i]['diffs'][j]['map_link_and_name'].text())
				if name=="":
					f.write(' ,')
				else:
					f.write(name+',')
				if link=="":
					f.write(' ,')
				else:
					f.write(link+',')
				f.write(self.diffs[i]['diffs'][j]['highest'].text()+',')
				f.write(self.diffs[i]['diffs'][j]['lowest'].text()+',')
				f.write(self.diffs[i]['diffs'][j]['average'].text()+',')
				f.write(self.diffs[i]['diffs'][j]['play_count'].text()+'\n')
				#all scores ['all_scores'][{'mods_name':'NM','mods_scores':[1,2,...]}{}{}{}]
				if not (self.diffs[i]['diff_name'] in ['FM','TB']):
					if len(self.diffs[i]['diffs'][j]['all_scores'])>0:
						k=0
						while k<len(self.diffs[i]['diffs'][j]['all_scores']):
							if k<len(self.diffs[i]['diffs'][j]['all_scores'])-1:
								f.write(str(self.diffs[i]['diffs'][j]['all_scores'][k])+',')
							else:
								f.write(str(self.diffs[i]['diffs'][j]['all_scores'][k])+'\n')
							k+=1
					else:
						f.write('\n')
				else:
					k=0
					while k<len(self.diffs[i]['diffs'][j]['all_scores']):
						if len(self.diffs[i]['diffs'][j]['all_scores'][k]['mods_scores'])>0:
							l=0
							while l<len(self.diffs[i]['diffs'][j]['all_scores'][k]['mods_scores'])-1:
								f.write(str(self.diffs[i]['diffs'][j]['all_scores'][k]['mods_scores'][l])+',')
								l+=1
							f.write(str(self.diffs[i]['diffs'][j]['all_scores'][k]['mods_scores'][l])+'\n')
						else:
							f.write('\n')
						k+=1
				j+=1
			f.write('#\n')
			i+=1
		f.close()
		#back up
		f=open(f"{filename}.txt",'r')
		F=f.readlines()
		f.close()

		all_files=os.listdir('./')
		backup_file_num=0
		while True:
			if not f"{filename}_backup_{backup_file_num}.txt" in all_files:
				break
			backup_file_num+=1

		f=open(f"{filename}_backup_{backup_file_num}.txt",'w')
		i=0
		while i<len(F):
			f.write(F[i])
			i+=1
		f.close()
		
		self.setWindowTitle(filename)

	def resizeEvent(self,event):
		width, height = event.size().width(), event.size().height()
		self.main_box.setGeometry(0,0,width,height)
		


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	Form = MyWidget()
	Form.show()
	sys.exit(app.exec_())
