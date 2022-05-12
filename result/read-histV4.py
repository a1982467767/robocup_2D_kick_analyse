#!/usr/bin/python
# coding=utf-8
import numpy as np 
import matplotlib.mlab as mlab 
import matplotlib.pyplot as plt 
import pandas 
import seaborn as sns 
import os
import shutil

# 参数依次为list,抬头,X轴标签,Y轴标签,XY轴的范围
def draw_hist(dataList, path, Xlabel, Ylabel, Xmin, Xmax, Ymin, Ymax, area):
	myListl1 = list()
	myListl2 = list()
	myListl3 = list()
	myListr1 = list()
	myListr2 = list()
	myListr3 = list()
	for elt in dataList: 
		myListl1 = []
		myListl2 = []
		myListl3 = []
		myListr1 = []
		myListr2 = []
		myListr3 = []
		for subelt in elt:
			myListl1.append(subelt[0][1]/10)#kick次数
			myListl2.append(subelt[0][6])
			myListl3.append(subelt[0][8])
			myListr1.append(subelt[1][1]/10)
			myListr2.append(subelt[1][6])
			myListr3.append(subelt[1][8])
		Title = elt[0][0][0] + "-vs-" + elt[0][1][0] + " area:" + str(area)
		#print(myListl1)
		#print(myListl2)
		#print(myListr1)
		#print(myListr2)
		#kick数据次数处理模块############################################################################
		#左方kick数据
		nl1, binsl1, patchesl1 = plt.hist(myListl1,30, normed=True, facecolor='yellowgreen', alpha=1)   
		mul1 =np.mean(myListl1) #计算均值 
		sigmal1 =np.std(myListl1) #计算标准差
		yl1 = mlab.normpdf(binsl1, mul1, sigmal1) #拟合一条最佳正态分布曲线y 
		plt.plot(binsl1, yl1, color="red", linewidth=2.5, linestyle="-", label=elt[0][0][0]) #绘制y的曲线 
		fl1 = np.polyfit(binsl1, yl1, sigmal1)#生产拟合函数
		pl1 = np.poly1d(fl1) 
		print(pl1)
		#右方kick数据
		nr1, binsr1, patchesr1 = plt.hist(myListr1,30, normed=True, facecolor='lightskyblue', alpha=1) 
		mur1 =np.mean(myListr1) #计算均值 
		sigmar1 = np.std(myListr1) #计算标准差 
		yr1 = mlab.normpdf(binsr1, mur1,sigmar1) #拟合一条最佳正态分布曲线y 
		plt.plot(binsr1, yr1, color="blue", linewidth=2.5, linestyle="-", label=elt[0][1][0]) #绘制y的曲线 
		fr1 = np.polyfit(binsr1, yr1, sigmar1)#生产拟合函数
		pr1 = np.poly1d(fr1) 
		print(pr1)	 
		#plt.subplot(121) 
		plt.xlabel(Xlabel)
		plt.xlim(Xmin,Xmax)
		plt.ylabel(Ylabel)
		plt.ylim(Ymin,Ymax)
		plt.title("num:"+Title)
		plt.subplots_adjust(left=0.15)
		plt.legend(loc="upper left") #线条标签
		plt.savefig("{}/kick_num/num:{}.jpg".format(path,Title))
		#plt.show()
		#plt.clf()
		plt.cla()
		#kick数据次数处理模块############################################################################

		#kick数据身前截球处理模块########################################################################
		nl2, binsl2, patchesl2 = plt.hist(myListl2,30, normed=True, facecolor='yellowgreen', alpha=1)   
		mul2 =np.mean(myListl2) #计算均值 
		sigmal2 =np.std(myListl2) #计算标准差
		yl2 = mlab.normpdf(binsl2, mul2, sigmal2) #拟合一条最佳正态分布曲线y 
		plt.plot(binsl2, yl2, color="red", linewidth=2.5, linestyle="-", label=elt[0][0][0]) #绘制y的曲线 
		fl2 = np.polyfit(binsl2, yl2, sigmal2)#生产拟合函数
		pl2 = np.poly1d(fl2) 
		print(pl2)
		#右方kick数据
		nr2, binsr2, patchesr2 = plt.hist(myListr2, 30, normed=True, facecolor='lightskyblue', alpha=1) 
		mur2 =np.mean(myListr2) #计算均值 
		sigmar2 = np.std(myListr2) #计算标准差 
		yr2 = mlab.normpdf(binsr2, mur2,sigmar2) #拟合一条最佳正态分布曲线y 
		plt.plot(binsr2, yr2, color="blue", linewidth=2.5, linestyle="-", label=elt[0][1][0]) #绘制y的曲线 
		fr2 = np.polyfit(binsr2, yr2, sigmar2)#生产拟合函数
		pr2 = np.poly1d(fr2) 
		print(pr2)	 
		#plt.subplot(121) 
		plt.xlabel(Xlabel)
		plt.xlim(60,90)
		plt.ylabel(Ylabel)
		plt.ylim(Ymin,1)
		plt.title("forward:"+Title)
		plt.subplots_adjust(left=0.15)
		plt.legend(loc="upper left") #线条标签
		plt.savefig("{}/kick_angle/forward:{}.jpg".format(path,Title))
		#plt.show()
		#plt.clf()
		plt.cla()
		#kick数据身前截球处理模块########################################################################

		#kick数据身前截球处理模块########################################################################
		nl3, binsl3, patchesl3 = plt.hist(myListl3, 20, normed=True, facecolor='yellowgreen',alpha=1)   
		mul3 =np.mean(myListl3) #计算均值 
		sigmal3 =np.std(myListl3) #计算标准差
		yl3 = mlab.normpdf(binsl3, mul3, sigmal3) #拟合一条最佳正态分布曲线y 
		plt.plot(binsl3, yl3, color="red", linewidth=2.5, linestyle="-", label=elt[0][0][0]) #绘制y的曲线 
		fl3 = np.polyfit(binsl3, yl3, sigmal3)#生产拟合函数
		pl3 = np.poly1d(fl3) 
		print(pl3)
		#右方kick数据
		nr3, binsr3, patchesr3 = plt.hist(myListr3, 20, normed=True, facecolor='lightskyblue', alpha=1) 
		mur3 =np.mean(myListr3) #计算均值 
		sigmar3 = np.std(myListr3) #计算标准差 
		yr3 = mlab.normpdf(binsr3, mur3,sigmar3) #拟合一条最佳正态分布曲线y 
		plt.plot(binsr3, yr3, color="blue", linewidth=2.5, linestyle="-", label=elt[0][1][0]) #绘制y的曲线 
		fr3 = np.polyfit(binsr3, yr3, sigmar3)#生产拟合函数
		pr3 = np.poly1d(fr3) 
		print(pr3)	 
		#plt.subplot(121) 
		plt.xlabel(Xlabel)
		plt.xlim(4,40)
		plt.ylabel(Ylabel)
		plt.ylim(Ymin,0.5)
		plt.title("less0.5:"+Title)
		plt.subplots_adjust(left=0.15)
		plt.legend(loc="upper left") #线条标签
		plt.savefig("{}/kick_dist/less0.5:{}.jpg".format(path,Title))
		#plt.show()
		#plt.clf()
		plt.cla()
		#kick数据身前截球处理模块########################################################################



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
		if elt[0] == '':#去空行
			continue
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
		try:
			elt[11] = float(elt[11])
		except:
			elt[11] = float(elt[11].split("/")[0])			 
		#print (elt)
		origin.append(elt)
    #['HfutEngine2018', '279', '143', '83.87', '16.13', '15.77', '19.35', '64.87', '1']
		#"team","kick","mulkick","forward","back","less0.5","0.5~0.8","high0.8","goal"
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
	for elt in alsub:
		print(elt)
	return alsub


############################################################################################################

if __name__ == "__main__":  #主程序入口
	root = os.getcwd()
	if root[-6:] == "result":
		root = root + "/"
	if root[-7:-1] != "result" :
		root = root + "result/"
	all_path = list()
	print (root)
	for root, subFolders, files in os.walk(root): #获取根path下的子文件夹，文件
		if subFolders != []:
			all_path = subFolders
			break
	print(all_path)
	for area in range(8):
		filename = "/kickAngleCount" + str(area) + ".txt"
		for path in all_path:
			path = root + path
			url = path + filename 
			if os.path.exists(path + "/kick_angle") and area == 0:  
				shutil.rmtree(path + "/kick_angle")#删除此目录中所有的数据，包括此目录
			if os.path.exists(path + "/kick_dist")and area == 0:  
				shutil.rmtree(path + "/kick_dist")
			if os.path.exists(path + "/kick_num")and area == 0: 
				shutil.rmtree(path + "/kick_num")
			if area == 0: 
				os.makedirs(path + "/kick_angle")
				os.makedirs(path + "/kick_dist")
				os.makedirs(path + "/kick_num")	 
			dataList = list()
			origin_data = getOriginData(url)
			length = len(origin_data)
			data_set = list()
			i = 0
			while(i < length):
				data_part = [origin_data[i],origin_data[i + 1]]
				i += 2
				data_set.append(data_part)
			data_set = sortByName(data_set)#按照队名进行排序
			dataList = getSecondData(data_set)
			draw_hist(dataList, path, 'Area', 'number', 20.0, 80.0, 0.0, 0.50, area)   # 直方图展示
