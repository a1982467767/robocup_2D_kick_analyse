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
import os,sys
import shutil
###########################################################################################################
def plt_bar(dataList, path):
		for elt in dataList: 
			print( elt)
		elt = dataList
		plt.figure(figsize=(13,8)) #图标长、宽
		n = 12 #x个数
		X = np.arange(n)+1
		#X是1,2,3,4,5,6,7,8,柱的个数 
		# numpy.random.uniform(low=0.0, high=1.0, size=None), normal 
		#uniform均匀分布的随机数，normal是正态分布的随机数，0.5-1均匀分布的数，一共有n个 
		lens = len(elt)
		teams = list()
		Y = list()
		cl = ['r','b','k','y','c','m','g']
		for i in range(lens):
			Y.append(elt[i][1:13])
			teams.append(elt[i][0])
		print (X)
		print (Y[0])
		for z in range(lens):
			plt.plot(X, Y[z], color=cl[z%7], linewidth=2.5, linestyle="-", label=teams[z])
			plt.scatter(X, Y[z],50, color =cl[z%7]) # 打点的意思
			for x,y in zip(X,Y[z]): 
				plt.text(x-0.175, y-0.5, '%s' % teams[z], ha='center', va= 'bottom', color=cl[z%7])
				break 
		if(lens<15):
			plt.legend(loc='upper right') #线条标签
		else:
			plt.legend(loc='upper right',fontsize=11) #线条标签
		#水平柱状图plt.barh，属性中宽度width变成了高度height 
		#打两组数据时用+ 
		#facecolor柱状图里填充的颜色 
		#edgecolor是边框的颜色 
		#想把一组数据打到下边，在数据前使用负号 
		#plt.bar(X, -Y2, width=width, facecolor='#ff9999', edgecolor='white') 
		#给图加text
		
		#画曲线2 
		#plt.plot(x, y2, color='blue', linewidth=5.0, linestyle='--') 
		#设置坐标轴范围 
		plt.xlim((0, 13)) 
		plt.ylim((0, 38)) 
		#设置坐标轴名称 
		plt.xlabel('kick by angle x * +-15°') 
		plt.ylabel('the distribution y %')
		 #设置坐标轴刻度 
		my_x_ticks = np.arange(0, 13, 1) 
		my_y_ticks = np.arange(0, 38, 2) 
		plt.xticks(my_x_ticks) 
		plt.yticks(my_y_ticks)
		title = "Angle Distribution"
		plt.grid(b=True, which='major', axis='x') # formats the grid line style of our graphs
		plt.savefig("{}.jpg".format(path))
		plt.show()
		#plt.clf()
		plt.cla()

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
	print( origin)
	return origin


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
	filename = "angle.txt"
	if len(sys.argv) == 2:
		filename = sys.argv[1]

	url = filename
	#dataList = list()
	origin_data = getOriginData(url)
	#data_set = sortByName(data_set)#按照队名进行排序
	#dataList = getSecondData(data_set)
	plt_bar(origin_data,"./"+filename[:-4])   # 直方图展示


