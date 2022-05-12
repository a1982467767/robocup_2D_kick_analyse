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
def getOriginData(url_str,area):
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
		if elt[1] == ' 0.3':#去标题
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
		try:
			elt[9] = float(elt[9])
		except:
			elt[9] = float(elt[9].split("/")[0])			 
		elt[10] = area		
		#print (elt)
		origin.append(elt)
	return origin

###########################################################################################################

if __name__ == "__main__":  #主程序入口
	root = os.getcwd() + "/"
	root = root + "All_Data"
	all_path = list()
	all_area_data = list()
	for area in range(8):
		filename = "/avgkickdataByDist"+ str(area) + ".txt"
		url = root + filename
		print (url)
		if not os.path.exists(url):  #跳过未生成的url
			print(url,"not found")
			continue 
                                                        
		origin_data = getOriginData(url,area)
		length = len(origin_data)
		data_set = list()#正向数据
		i = 0
		while(i < length):
			data_part = [origin_data[i],origin_data[i + 1]]
			i += 2
			data_set.append(data_part)
		for elt in data_set:
			all_area_data.append(elt) #数据合并

	all_area_data = sorted(all_area_data, key=lambda x:(x[0][0],x[1][0])) #对主列表排序
	filename1 = "/T_avgkickdataByDist.txt"
	if os.path.exists("./All_Data"+filename1):#每次生成新的文件替换之前的文件 
		os.remove("./All_Data"+filename1)
	file_w = open( "./All_Data"+filename1,"a+")
	#print (all_area_data)
	#操作数据输出3
	for data in all_area_data: 
		s = str(data[0]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择 
		s = s.replace("'",'').replace(',','\t') +'\n' #去除单引号，逗号，每行末尾追加换行符 
		file_w.write(s)
		s = str(data[1]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择 
		s = s.replace("'",'').replace(',','\t') +'\n' #去除单引号，逗号，每行末尾追加换行符
		file_w.write(s)
	file_w.close()


