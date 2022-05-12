#!/usr/bin/env python3
# -*-encoding: utf-8 -*-
# author: Qian Jipeng(C)
# 对上一步生成的各个球队的txt文件进行读取，并按照分区画图
# 和"sep_gather.py", "start.sh" 一起用

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# filepaths = [ i + '.txt' for i in['MT2018SS','MT2018GS','MT2018SJB','HELIOS2011','HELIOS2012','HELIOS2013','HELIOS2014','HELIOS2015','HELIOS2016','HELIOS2017','HELIOS2018', 'Gliders2013','Gliders2014','Gliders2015','Gliders2016','CYRUS','CYRUS2014','CYRUS2018','HfutEngine2017','HfutEngine2018','Oxsy']]

# for filepath in filepaths:

team = sys.argv[1][:-4]
area = sys.argv[2]
result =  team
if not os.path.exists( result ):  #创建根目录
	os.makedirs( result )

#color_list = [ 'darkcyan', 'cyan', 'darkturquoise', 'deepskyblue', 'skyblue','steelblue', 'cornflowerblue', 'royalblue', 'dodgerblue', 'honeydew','palegreen','c','lightcyan']
#color_list = [ 'red','maroon', 'brown' ,'rosybrown', 'lightcoral',  'salmon', 'darksalmon', 'orangered', 'lightsalmon', 'chocolate', 'sandybrown', 'linen']
color_list = [ 'steelblue', 'sandybrown', 'limegreen', 'indianred', 'plum',  'darkgrey', 'lightpink', 'burlywood', 'khaki', 'lightblue', 'skyblue','sandybrown']
with open(team + '.txt', "r") as f:
	# 获取文件的每一行
	count = 0
	angle_count = []  # 用来存对应的line
	by_angle = []
	by_dist = []
	# lines = []

	# 遍历每一行
	for line in f:
		count += 1  # count 行数

		# line = f.readline()		# 最后一个元素有换行符， 待处理
		# lines.append(line)			# 存每一行

		# print(line)		# 24

		# 取每行最后一个字符，就是分区编号
		# print(line.split("	 ")[-1])

		'''
		TODO:
			加个循环，遍历八个分区(shell 实现)
		'''

		#areas = [0, 1, 2, 3, 4, 5, 6, 7]

		#for area in areas:

			#lines = []

		if line.split("	 ")[-1].rstrip() == str(area):  # 3行数据
			
			times = 0		#用来计数，达到3就画图显示一下title
			
			#lines.append(line)
			# 新建一张画布,指定长宽比
			#fig = plt.figure(1, figsize = (5,2))
			fig  = plt.figure(1, figsize = (25,10))



			####################################################################################### 画 kick_by_dist

			if count == (1 + int(sys.argv[2])):
				
				times += 1

				tmp2 = line.split("	 ")[0] + line.split("	 ")[-1].rstrip()
				line.split("	 ")[0] = tmp2

				del line.split("	 ")[-1]
				del line.split("	 ")[-2]

				by_dist = line.split("	 ")[:-2]
				# print(by_dist)
				total = 0.0
				# 换成百分比
				new_by_dist = [tmp2]
				for i in by_dist[1:]:
					i = float(i)
					new_by_dist.append(i)
				# print(new_by_dist)			# ['CYRUS0', 0.0, 0.1, 0.07, 0.07, 0.13, 0.17, 0.18, 0.28]

				df3 = pd.DataFrame(new_by_dist[1:], index=['0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0'])

				# print(df3)
				# print(df2)
				for i in range(0,8):
					total += float(df3.iat[i, 0])
				for i in range(0,8):
					df3.iat[i, 0] = float(format(float(df3.iat[i, 0]) / total , '.3f'))  # 小数点后两位
				ax3 = fig.add_subplot(311)

				data3 = np.array(df3.T)		# 转置

				X3 = ['0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0']

				Sum3 = 0
				#print(data3.shape[0])
				for i in range(data3.shape[1]):  # lie shu
				
					Sum3 += data3[0][i]
					# print(Sum3)

					# print(data3[:,0])		# [0.   0.1  0.07 0.07 0.13 0.17 0.18 0.28]

					ax3.barh(0, data3[0][i], height= 0.8, left=Sum3 - data3[0][i], color=color_list[i], alpha= 0.5,linewidth = 0)  # left	 参数来控制叠加
					plt.yticks([-0.6,0.6])
					plt.xticks([-0,1.0])
					#plt.legend(loc='upper left', fontsize= 6)
					plt.text(-0.12,-0.2,' Dist',va= 'bottom', fontsize=50)
					plt.text(0.3,0.6,'1:0.4  2:0.5  3:0.6  4:0.7  5:0.8  6:0.9  7:1.0', va= 'top', fontsize=30)
					
					# 打上数值
					if data3[0][i] > 0.05:	
						
						# plt.text(x,y,s,ha,va...)		x,y 是位置坐标
						plt.text(Sum3 - (data3[0][i] / 2.0),-0.2,'%.1f'%((data3[0][i]) * 100),ha='center', va= 'bottom', fontsize=50)
						

			###################################################################################### 画 kick_by_angle

			if count == (9 + int(area)):
				
				times += 1
				
				tmp1 = line.split("	 ")[0] + line.split("	 ")[-1].rstrip()
				line.split("	 ")[0] = tmp1

				# 删除不要的数据
				del line.split("	 ")[-1]
				del line.split("	 ")[-2]
				#print (line)
				by_angle = line.split("	 ")[:-2]
				#print (by_angle)
				# print(by_angle)

				# 换成百分比
				total = 0.0
				new_by_angle = [tmp1]  # CYRUS0
				for i in by_angle[1:]:
					i = float(i)
					new_by_angle.append(i)
				# print(new_by_angle)		# ['CYRUS0', '0.47', '0.20', '0.11', '0.05', '0.04', '0.03', '0.02', '0.03', '0.01', '0.02', '0.02', '0.01']
				
				df2 = pd.DataFrame(new_by_angle[1:],
								   index=['dir15', 'dir30', 'dir45', 'dir60', 'dir75', 'dir90', 'dir105', 'dir120',
										  'dir135', 'dir150', 'dir165', 'dir180'])
				# print(df2)
				for i in range(0,12):
					total += float(df2.iat[i, 0])

				for i in range(0,12):
					df2.iat[i, 0] = float(format(float(df2.iat[i, 0]) / total , '.3f'))  # 小数点后两位
					#print (total ,df2.iat[i, 0])
				data2 = np.array(df2.T)
				# print(data2)

				ax2 = fig.add_subplot(312)

				X2 = ['dir15', 'dir30', 'dir45', 'dir60', 'dir75', 'dir90', 'dir105', 'dir120', 'dir135', 'dir150',
					  'dir165', 'dir180']

				Sum2 = 0
				for i in range(data2.shape[1]):  # hang shu

					Sum2 += data2[0][i]
					# print(Sum2)

					ax2.barh(0, data2[0][i], height= 0.8, left=Sum2 - data2[0][i], color=color_list[i], alpha= 0.5,linewidth = 0)  # left	 参数来控制叠加
					plt.yticks([-0.6,0.6])
					plt.xticks([-0,1.0])
					#plt.legend(loc='upper left', fontsize= 6)
					plt.text(-0.14,-0.2,'Angle',va= 'bottom', fontsize=50)
					plt.text(0.2,0.6,'1:dir15 2:dir30 3:dir45 4:dir60 ------ 11:dir165 12:dir180', va= 'top', fontsize=30)
					# 打上数值
					if data2[0][i] > 0.05:	
						
						# plt.text(x,y,s,ha,va...)		x,y 是位置坐标
						plt.text(Sum2 - (data2[0][i] / 2.0),-0.2,'%.1f'%((data2[0][i])*100),ha='center', va= 'bottom', fontsize=50)


			######################################################################################  画 angle_count --- the start

			if count == (17 + int(sys.argv[2])):
				
				times += 1
				
				# print(line.split("	 ")[3:6])		# pass dribble hold
				angle_count.append(line.split("	 ")[0] + line.split("	 ")[-1].rstrip())  # 队名处理加上分区

				angle_count.append(line.split("	 ")[2])
				angle_count.append(line.split("	 ")[3])
				angle_count.append(line.split("	 ")[4])

				# print(angle_count)		# ['CYRUS0', '13.31', '21.02', '13.0']  angle_count 数据

				df1 = pd.DataFrame(angle_count[1:], index=['pass', 'dribble', 'hold'])

				# print(df1)
				# 求百分比(占其中3个总数)
				total = float(df1.iat[0, 0]) + float(df1.iat[1, 0]) + float(df1.iat[2, 0])  # 注意通过索引来的是str类型

				df1.iat[0, 0] = float(format(float(df1.iat[0, 0]) / total , '.3f'))  # 小数点后两位
				df1.iat[1, 0] = float(format(float(df1.iat[1, 0]) / total , '.3f'))
				df1.iat[2, 0] = float(format(float(df1.iat[2, 0]) / total , '.3f'))

				# print(df1['pass':'hold'])

				ax1 = fig.add_subplot(313)

				data1 = np.array(df1.T)

				X1 = ['pass', 'dribble', 'hold']

				Sum1 = 0
				for i in range(data1.shape[1]):  # hang shu

					Sum1 += data1[0][i]
					# print(Sum2)

					ax1.barh(0, data1[0][i], height= 0.8, left=Sum1 - data1[0][i], color=color_list[i], alpha= 0.5)  # left	 参数来控制叠加
					plt.yticks([-0.6,0.6])
					plt.xticks([-0,1.0])
					#plt.legend(loc='upper left', fontsize= 6)
					plt.text(-0.14,-0.2,'Action',va= 'bottom', fontsize=50)
					plt.text(0.4,0.6,'1:pass 2:dribble 3:hold', va= 'top', fontsize=30)
					# 打上数值
					if data1[0][i] > 0:	
						
						# plt.text(x,y,s,ha,va...)		x,y 是位置坐标
						plt.text(Sum1 - (data1[0][i] / 2.0),-0.2,'%.1f'%((data1[0][i]) * 100),ha='center', va= 'bottom', fontsize=50)
			
			
			
			#path = os.path.abspath(sys.argv[3])		# 接收来自bash 的文件夹名
			
			#print(path)
			
			file_name = result +"/" + line.split("	 ")[0] + line.split("	 ")[-1].rstrip() + '.png'
			plt.savefig(file_name)
			#plt.savefig("111.jpg")
			
