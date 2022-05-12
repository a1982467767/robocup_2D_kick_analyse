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
def plt_bar(dataList, path ,area):
	for elt in dataList: 
		print( elt)
		fig = plt.figure(figsize=(9,6)) #图标长、宽
		#设置坐标轴范围 
		plt.xlim((0.3, 1.1)) 
		plt.ylim((0, 28)) 
		#设置坐标轴名称 
		plt.xlabel('kick by dist x') 
		plt.ylabel('the distribution y %')
		 #设置坐标轴刻度 
		my_x_ticks = np.arange(0.3, 1.0, 0.1) 
		my_y_ticks = np.arange(0, 28, 2) 
		plt.xticks(my_x_ticks) 
		plt.yticks(my_y_ticks)
		#球场建模================================================================================================end
		n = 8 #x个数
		X = (np.arange(n)+3)/10
		#X是1,2,3,4,5,6,7,8,柱的个数 
		# numpy.random.uniform(low=0.0, high=1.0, size=None), normal 
		#uniform均匀分布的随机数，normal是正态分布的随机数，0.5-1均匀分布的数，一共有n个 
		Y1 = elt[0][1:9]
		Y2 = elt[1][1:9]
		team = [elt[0][0],elt[1][0]]
		plt.bar(X-0.035,Y1,width = 0.035,facecolor = 'lightskyblue',edgecolor = 'white') 
		#width:柱的宽度 
		plt.bar(X,Y2,width = 0.035,facecolor = 'yellowgreen',edgecolor = 'white') 

		plt.plot(X, Y1, color="blue", linewidth=2.5, linestyle="-", label=team[0])
		plt.plot(X, Y2, color="red",  linewidth=2.5, linestyle="-", label=team[1])
		plt.scatter(X, Y1,50, color ='blue') # 打点的意思
		plt.scatter(X, Y2,50, color ='red') # 打点的意思
		plt.legend(loc="upper left") #线条标签
		#水平柱状图plt.barh，属性中宽度width变成了高度height 
		#打两组数据时用+ 
		#facecolor柱状图里填充的颜色 
		#edgecolor是边框的颜色 
		#想把一组数据打到下边，在数据前使用负号 
		#plt.bar(X, -Y2, width=width, facecolor='#ff9999', edgecolor='white') 
		#给图加text 
		for x,y in zip(X,Y1): 
			plt.text(x-0.0175, y+0.5, '%.2f' % y, ha='center', va= 'bottom') 
		for x,y in zip(X,Y2): 
			plt.text(x+0.0175, y+0.5, '%.2f' % y, ha='center', va= 'bottom') 
		#画曲线2 
		#plt.plot(x, y2, color='blue', linewidth=5.0, linestyle='--') 

		title = "moreDist: " + team[0] + "-vs-" + team[1] + " Area:" + str(area)
		plt.title(title)
		plt.savefig("{}/kick_dist/moreDist:{}area:{}.jpg".format(path,title,str(area)))
		#plt.show()
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
		elt[9] = float(elt[9])	
		try:
			elt[10] = float(elt[10])
		except:
			elt[10] = float(elt[10].split("/")[0])			 
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
def getSecondData(data_set): #将数据进行划分，相同队伍的比赛划为一组数据
	length = len(data_set)
	i = 0	
	new_count = data_set[0]
	alsub = list()
	sub = list()
	#print(data_set)
	while i  < length :
		if new_count[0][0] == data_set[i][0][0] and new_count[1][0] == data_set[i][1][0]:
			sub.append(data_set[i])
		else:
			alsub.append(sub)
			sub = [] #清空子数组
			new_count = data_set[i]
		i += 1
	if len(sub) > 0:
		sub.append(new_count)
		alsub.append(sub)
	#for elt in alsub:
	#	print(elt)
	return alsub


############################################################################################################

if __name__ == "__main__":  #主程序入口
	root = os.getcwd() + "/"
	if root[-7:-1] != "result":
		root = root + "result/"
	all_path = list()
	for root, subFolders, files in os.walk(root): #获取根path下的子文件夹，文件
		if subFolders != []:
			all_path = subFolders
			break
	print(all_path)
	for area in range(8):
		filename = "/avgkickdataByDist" + str(area) + ".txt"
		for path in all_path:
			path = root + path
			url = path + filename
			if not os.path.exists(url):  #跳过未生成的url
				continue 
			if not os.path.exists(path + "/kick_dist"):  #创建根目录
				os.makedirs(path + "/kick_dist")
			#dataList = list()
			origin_data = getOriginData(url)
			length = len(origin_data)
			data_set = list()
			i = 0
			while(i < length):
				data_part = [origin_data[i],origin_data[i + 1]]
				i += 2
				data_set.append(data_part)
			#data_set = sortByName(data_set)#按照队名进行排序
			#dataList = getSecondData(data_set)
			plt_bar(data_set,path,area)   # 直方图展示


