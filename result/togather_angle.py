#!/usr/bin/python3
# coding=utf-8
"""
Copyright (C) 2018 YuShan2D SunChen 
"""
import numpy as np 
import matplotlib.mlab as mlab 
import matplotlib.pyplot as plt 
import pandas 
import seaborn as sns 
import os
import shutil

###########################################################################################################
def getOriginData(url_str):
	file_r = open(url_str,"r")
	content = file_r.read()
	file_r.close()
	content = content.split("\n")
	origin = list()
	for elt in content:
		#print (elt)
		elt=elt.split("\t")
		if len(elt) == 1: #去=====
			continue
		if elt[0] == '':#去空行
			continue
		if elt[1] == 'dir15':#去标题
			continue
		elt[0] = elt[0].lstrip()
		elt[1] = float(elt[1])
		elt[2] = float(elt[2])
		elt[3] = float(elt[3])
		elt[4] = float(elt[4])
		elt[5] = float(elt[5])
		elt[6] = float(elt[6])	
		elt[7] = float(elt[7])
		elt[8] = float(elt[8])
		elt[9] = float(elt[9])
		elt[10] = float(elt[10])
		elt[11] = float(elt[11])
		elt[12] = float(elt[12])	
		try:
			elt[13] = float(elt[13])
		except:
			elt[13] = float(elt[13].split("/")[0])			 
		#print (elt)
		origin.append(elt)
	return origin


###########################################################################################################
def sortByName(data_set):  #这里对各队进行排序
	data_set1 = list()
	for elt in data_set:
		elt = sorted(elt, key=lambda x:x[0],reverse=True) #对字列表排序
		data_set1.append(elt)
	data_set1 = sorted(data_set1, key=lambda x:(x[0][0],x[1][0])) #对主列表排序
	#for elt1 in data_set1:  #通过排序,可使得yushan永远在数据的右边
	#	print (elt1)
	return data_set1

###########################################################################################################
def sortByName2(data_set):  #这里对各队进行排序
	data_set2 = list()
	for elt in data_set:
		elt = sorted(elt, key=lambda x:x[0]) #对字列表排序
		data_set2.append(elt)
	data_set2 = sorted(data_set2, key=lambda x:(x[0][0],x[1][0])) #对主列表排序
	#for elt1 in data_set1:  #通过排序,可使得yushan永远在数据的右边
	#	print (elt1)
	return data_set2
	
###########################################################################################################
def getSecondData(data_set): #将数据进行划分，相同队伍的比赛划为一组数据
	length = len(data_set)
	i = 1	
	new_count = data_set[0]
	alsub = list()
	sub = [data_set[0]]
	#print(data_set)
	while i  < length :
		if new_count[0][0] == data_set[i][0][0] and new_count[1][0] == data_set[i][1][0]:
			sub.append(data_set[i])
		else:
			alsub.append(sub)
			sub = [data_set[i]] 
			new_count = data_set[i]
		i += 1
	alsub.append(sub)
	return alsub

############################################################################################################

if __name__ == "__main__":  #主程序入口
	root = os.getcwd() + "/"
	root = root + "result/"
	all_path = list()
	for root, subFolders, files in os.walk(root): #获取根path下的子文件夹，文件
		if subFolders != []:
			all_path = subFolders
			break
	print(all_path)
	if 1:
		for area in range(8):
			filename = "/kickdataByAngle"+ str(area) + ".txt"
			all_data = list()
			all_data2 = list()
			for path in all_path:
				path = root + path
				url = path + filename
				print (url)
				if not os.path.exists(url):  #跳过未生成的url
					continue 
				if not os.path.exists("./All_Data"):  #创建根目录
					os.makedirs("./All_Data")
				                                                                                                     
				origin_data = getOriginData(url)
				length = len(origin_data)
				data_set = list()#正向数据
				data_set2 = list()#反向数据
				i = 0
				while(i < length):
					data_part = [origin_data[i],origin_data[i + 1]]
					i += 2
					data_set.append(data_part)
				data_set2 = sortByName2(data_set)##反向数据
				data_set = sortByName(data_set)#按照队名进行排序
				for elt in data_set:
					all_data.append(elt) #数据合并
				for elt in data_set2:
					all_data2.append(elt) #数据合并
			all_data = sortByName(all_data)#按照队名进行排序
			all_data = getSecondData(all_data)

			all_data2 = sortByName2(all_data2)#按照队名进行排序
			all_data2 = getSecondData(all_data2)
			for elt in all_data2:
				all_data.append(elt)
			if os.path.exists("./All_Data"+filename):  #创建根目录
				os.remove("./All_Data"+filename)#删除
			file_w = open( "./All_Data"+filename,"a+")
			#操作数据输出3
			for data in all_data:
				for i in range(len(data)): 
					s = str(data[i][0]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择 
					s = s.replace("'",'').replace(',','\t') +'\n' #去除单引号，逗号，每行末尾追加换行符 
					file_w.write(s)
					s = str(data[i][1]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择 
					s = s.replace("'",'').replace(',','\t') +'\n' #去除单引号，逗号，每行末尾追加换行符
					file_w.write(s)
			file_w.close()


